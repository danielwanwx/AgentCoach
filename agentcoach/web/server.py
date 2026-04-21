"""Stdlib HTTP server for the Her-inspired web UI.

Routes (JSON unless noted):

    POST /api/session/start    {mode, topic_id, user_id?}  -> {session_id, opening}
    POST /api/session/turn     {session_id, user_text}     -> {coach_text}
    POST /api/session/end      {session_id, survey?}       -> assessment payload
    GET  /api/session/{id}/report                          -> assessment payload
    GET  /api/topics                                       -> [{id, name, domain}]
    GET  /*                                                -> static file from frontend/

No new deps — uses only `http.server`. The same Coach/Scorer/AnalyticsStore
wired into the CLI back the endpoints here, so the growth curve a user
sees in the web report is the same one they would see from `progress` at
the terminal.

Launch:
    python -m agentcoach.web.server               # listens on 8765
    python -m agentcoach.web.server --port 9000

When no LLM credentials are configured the server falls back to a
deterministic scripted coach so the UI stays explorable offline.
"""
from __future__ import annotations

import argparse
import json
import os
import threading
import uuid
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from agentcoach.analytics.store import AnalyticsStore
from agentcoach.analytics.scorer import Scorer
from agentcoach.analytics.skill_profile import build_skill_profile
from agentcoach.kb.store import KnowledgeStore
from agentcoach.coaching.coach import Coach
from agentcoach.syllabus.loader import SyllabusLoader
from agentcoach.log import get_logger

logger = get_logger()

ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = ROOT / "frontend"
STATIC_MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
}


# ────────────────────────── state ──────────────────────────

@dataclass
class WebSession:
    session_id: str
    user_id: str
    mode: str
    topic_id: str
    topic_name: str
    domain: str
    coach: Optional[Coach] = None
    kb_store: Optional[KnowledgeStore] = None
    opening: str = ""
    closed: bool = False
    assessment: dict = field(default_factory=dict)
    survey: dict = field(default_factory=dict)
    demo_turn: int = 0
    demo_transcript: list = field(default_factory=list)


class ServerState:
    """Shared process-wide state; instantiated once per server."""

    def __init__(self, data_dir: Path, demo_mode: bool = False):
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir = data_dir
        self.demo_mode = demo_mode
        self.analytics = AnalyticsStore(db_path=str(data_dir / "analytics.db"))
        self.sessions: dict[str, WebSession] = {}
        self.lock = threading.Lock()
        self.syllabus = SyllabusLoader()
        self._coach_llm = None
        self._scorer_llm = None

    # Lazy LLM init so a missing key does NOT crash startup — only kicks in
    # the first time someone actually opens a real (non-demo) session.
    def coach_llm(self):
        if self._coach_llm is None:
            self._coach_llm = _make_llm(role="coaching")
        return self._coach_llm

    def scorer_llm(self):
        if self._scorer_llm is None:
            self._scorer_llm = _make_llm(role="scoring")
        return self._scorer_llm


def _make_llm(role: str):
    try:
        from agentcoach.llm.router import LLMRouter
        return LLMRouter.from_env().get(role)
    except Exception as e:
        logger.warning("llm_init_failed", role=role, error=str(e))
        return None


# ─────────────────── topic catalog (minimal) ───────────────────

TOPICS = [
    {"id": "system_design.url_shortener", "name": "URL Shortener", "domain": "system_design"},
    {"id": "system_design.ticketmaster", "name": "Ticketmaster", "domain": "system_design"},
    {"id": "system_design.distributed_rate_limiter", "name": "Distributed Rate Limiter", "domain": "system_design"},
    {"id": "system_design.message_queues", "name": "Message Queues (Kafka)", "domain": "system_design"},
    {"id": "system_design.stock_exchange", "name": "Stock Exchange", "domain": "system_design"},
]
MODES = ["learn", "reinforce", "mock_system_design"]

DEMO_SCRIPT = [
    "Great — let's design a URL shortener together. Before we dive in, what scale are you designing for, roughly?",
    "Good starting point. Now walk me through the write path. A user hits POST /shorten — what happens next?",
    "You mentioned a hash. What properties does that hash need, and what's the risk if two inputs collide?",
    "Let's talk storage. If we hit 500M shortens a year, how do you size the keyspace and the database?",
    "Last one: how would you add rate limiting without breaking the 99.9% latency target?",
]


# ─────────────────── request helpers ───────────────────

def _json_body(handler: "Handler") -> dict:
    try:
        length = int(handler.headers.get("Content-Length", "0"))
    except ValueError:
        length = 0
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


def _write_json(handler: "Handler", status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def _serve_static(handler: "Handler", relpath: str) -> None:
    # Default index
    if relpath in ("", "/"):
        relpath = "index.html"
    relpath = relpath.lstrip("/")

    fs_path = (FRONTEND_DIR / relpath).resolve()
    if not str(fs_path).startswith(str(FRONTEND_DIR.resolve())):
        handler.send_error(403)
        return
    if not fs_path.exists() or not fs_path.is_file():
        handler.send_error(404)
        return
    mime = STATIC_MIME.get(fs_path.suffix, "application/octet-stream")
    data = fs_path.read_bytes()
    handler.send_response(200)
    handler.send_header("Content-Type", mime)
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    # Dev server: never cache static assets so CSS/JS/HTML edits show up on reload.
    handler.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
    handler.send_header("Pragma", "no-cache")
    handler.send_header("Expires", "0")
    handler.end_headers()
    handler.wfile.write(data)


# ─────────────────── coach lifecycle ───────────────────

def _resolve_topic(topic_id: str) -> tuple[str, str, str]:
    for t in TOPICS:
        if t["id"] == topic_id:
            return t["id"], t["name"], t["domain"]
    # Allow free-form ids: extract domain from prefix, name from tail.
    if "." in topic_id:
        domain, tail = topic_id.split(".", 1)
        return topic_id, tail.replace("_", " ").title(), domain
    return topic_id, topic_id.title(), "system_design"


def _make_kb(state: ServerState, session_id: str, topic_name: str, domain: str) -> KnowledgeStore:
    kb_path = state.data_dir / f"session-{session_id}.kb.db"
    kb = KnowledgeStore(db_path=str(kb_path), use_vectors=False)
    kb.add_chunk(
        content=(
            f"Reference notes on {topic_name}. "
            f"Focus on requirements, core architecture, scale estimation, "
            f"deep-dive on the hottest component, and the key trade-offs."
        ),
        source="seed", section=topic_name, category=domain,
    )
    return kb


def _start_session(state: ServerState, body: dict) -> dict:
    mode = body.get("mode") or "mock_system_design"
    if mode not in MODES:
        mode = "mock_system_design"
    topic_id_raw = body.get("topic_id") or "system_design.url_shortener"
    topic_id, topic_name, domain = _resolve_topic(topic_id_raw)
    user_id = (body.get("user_id") or "web-guest").strip() or "web-guest"

    session_id = uuid.uuid4().hex[:12]
    ws = WebSession(
        session_id=session_id, user_id=user_id, mode=mode,
        topic_id=topic_id, topic_name=topic_name, domain=domain,
    )

    llm = state.coach_llm()
    if llm is None or state.demo_mode:
        ws.opening = (
            f"Great — let's work on {topic_name}. "
            "Walk me through how you'd start."
        )
    else:
        try:
            kb = _make_kb(state, session_id, topic_name, domain)
            ws.kb_store = kb
            coach = Coach(
                llm=llm, mode=mode, kb_store=kb,
                topic_id=topic_id, topic_name=topic_name,
                memory_context=(
                    "\n\nThis session is spoken aloud in the browser. "
                    "Reply in at most 3 short spoken sentences (under 60 words). "
                    "No markdown, no bullets. One idea per turn, then ask the "
                    "candidate exactly one thing."
                ),
            )
            ws.opening = coach.start()
            ws.coach = coach
        except Exception as e:
            logger.error("coach_start_failed", error=str(e))
            ws.opening = (
                f"Let's get started on {topic_name}. "
                "Can you walk me through the core requirements first?"
            )

    with state.lock:
        state.sessions[session_id] = ws
    return {
        "session_id": session_id,
        "opening": ws.opening,
        "topic_id": topic_id,
        "topic_name": topic_name,
        "mode": mode,
    }


def _turn(state: ServerState, body: dict) -> dict:
    sid = body.get("session_id")
    text = (body.get("user_text") or "").strip()
    with state.lock:
        ws = state.sessions.get(sid)
    if not ws:
        return {"error": "unknown session"}
    if not text:
        return {"coach_text": ""}

    if ws.coach is None:
        # Demo fallback — rotate through canned follow-ups so the UI demo
        # still feels like a conversation. We also stash the exchange so
        # end-of-session scoring has something to look at.
        ws.demo_transcript.append({"role": "user", "content": text})
        line = DEMO_SCRIPT[min(ws.demo_turn, len(DEMO_SCRIPT) - 1)]
        ws.demo_turn += 1
        ws.demo_transcript.append({"role": "coach", "content": line})
        return {"coach_text": line}

    try:
        reply = ws.coach.respond(text)
    except Exception as e:
        logger.error("coach_respond_failed", error=str(e))
        reply = "Let me rephrase — can you tell me more about your high-level design?"
    return {"coach_text": reply}


def _end(state: ServerState, body: dict) -> dict:
    sid = body.get("session_id")
    with state.lock:
        ws = state.sessions.get(sid)
    if not ws:
        return {"error": "unknown session"}
    ws.survey = body.get("survey") or {}

    # Compute assessment — prefer the real scorer on the transcript, fall
    # back to a plausible stub payload if no LLM is available.
    scorer_llm = state.scorer_llm()
    pre_mastery = state.analytics.get_mastery(ws.user_id, ws.topic_id)

    assessment = _score_or_stub(ws, scorer_llm, state.analytics)
    post_mastery = state.analytics.get_mastery(ws.user_id, ws.topic_id)

    profile = build_skill_profile(state.analytics, ws.user_id, ws.domain, limit=20)
    growth = {
        name: info["history"]
        for name, info in (profile.get("dimensions") or {}).items()
    }

    assessment.update({
        "session_id": sid,
        "topic_id": ws.topic_id,
        "topic_name": ws.topic_name,
        "mode": ws.mode,
        "mastery_before": pre_mastery,
        "mastery_after": post_mastery,
        "mastery_delta": post_mastery - pre_mastery,
        "growth": growth,
        "survey": ws.survey,
    })
    ws.assessment = assessment
    ws.closed = True
    return assessment


def _score_or_stub(ws: WebSession, llm, analytics: AnalyticsStore) -> dict:
    """Run the Scorer on the transcript and persist the assessment."""
    if ws.coach and llm is not None:
        try:
            from agentcoach.syllabus.loader import SyllabusLoader
            scorer = Scorer(llm, kb_store=ws.kb_store, syllabus=SyllabusLoader())
            scored = scorer.score_session(
                ws.coach.history, mode=ws.mode, topic_id=ws.topic_id,
            )
            if scored:
                primary = scored[0]
                overall = float(primary.get("overall_score") or 0.0)
                dims = primary.get("dimensions") or []
                strengths = primary.get("strengths") or []
                areas = primary.get("areas_to_improve") or []
                analytics.record_score(
                    ws.user_id, ws.topic_id,
                    int(primary.get("score_delta") or 0),
                    ws.mode, primary.get("evidence") or "",
                )
                analytics.record_assessment(
                    user_id=ws.user_id, topic_id=ws.topic_id, domain=ws.domain,
                    mode=ws.mode, overall_score=overall,
                    dimensions=dims, strengths=strengths, areas_to_improve=areas,
                    session_id=ws.session_id,
                )
                return {
                    "overall_score": overall, "dimensions": dims,
                    "strengths": strengths, "areas_to_improve": areas,
                }
        except Exception as e:
            logger.error("scorer_failed", error=str(e))

    # Deterministic stub so the UI still renders a report end-to-end.
    # We slightly randomize dims *based on the session id* so repeated
    # demo runs produce a visible growth curve across sessions rather
    # than a flat line.
    import hashlib
    seed = int(hashlib.sha1((ws.session_id or "x").encode()).hexdigest()[:8], 16)
    bump = lambda base, salt: max(1, min(5, base + ((seed >> salt) & 0x3) - 1))  # noqa: E731
    dims = [
        {"name": "requirements", "score": bump(3, 0), "evidence": "Clarified scale + traffic assumptions."},
        {"name": "high_level_design", "score": bump(3, 2), "evidence": "Listed components but thin on data flow."},
        {"name": "deep_dive", "score": bump(2, 4), "evidence": "Touched hashing but skimmed collision handling."},
        {"name": "scalability", "score": bump(3, 6), "evidence": "Sized for 500M writes/year with numbers."},
        {"name": "tradeoffs", "score": bump(3, 8), "evidence": "Acknowledged CAP implications only when prompted."},
    ]
    overall = round(sum(d["score"] for d in dims) / len(dims), 1)
    strengths = [
        "Grounded design in concrete numbers.",
        "Named the primary component cleanly.",
    ]
    areas = [
        "Go one level deeper on the hot component (sharding, cache layer).",
        "State trade-offs proactively rather than on request.",
    ]
    # Persist the stub so the growth curve and mastery bar are populated
    # across repeated practice sessions, even without a real LLM.
    try:
        analytics.record_score(
            ws.user_id, ws.topic_id,
            int((overall - 2.0) * 5), ws.mode,
            "demo-mode stub assessment",
        )
        analytics.record_assessment(
            user_id=ws.user_id, topic_id=ws.topic_id, domain=ws.domain,
            mode=ws.mode, overall_score=overall,
            dimensions=dims, strengths=strengths, areas_to_improve=areas,
            session_id=ws.session_id,
        )
    except Exception as e:
        logger.warning("stub_persist_failed", error=str(e))
    return {
        "overall_score": overall,
        "dimensions": dims,
        "strengths": strengths,
        "areas_to_improve": areas,
    }


# ─────────────────── request handler ───────────────────

class Handler(BaseHTTPRequestHandler):
    state: ServerState  # injected by server factory

    # quieter logging — only real errors
    def log_message(self, fmt, *args):  # noqa: N802 (http.server override)
        if "error" in fmt.lower():
            super().log_message(fmt, *args)

    def do_OPTIONS(self):  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/topics":
            return _write_json(self, 200, {"topics": TOPICS, "modes": MODES})
        if path.startswith("/api/session/") and path.endswith("/report"):
            sid = path.split("/")[3]
            with self.state.lock:
                ws = self.state.sessions.get(sid)
            if not ws or not ws.assessment:
                return _write_json(self, 404, {"error": "not found"})
            return _write_json(self, 200, ws.assessment)
        return _serve_static(self, path)

    def do_POST(self):  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/session/start":
            return _write_json(self, 200, _start_session(self.state, _json_body(self)))
        if path == "/api/session/turn":
            return _write_json(self, 200, _turn(self.state, _json_body(self)))
        if path == "/api/session/end":
            return _write_json(self, 200, _end(self.state, _json_body(self)))
        _write_json(self, 404, {"error": "not found"})


def serve(port: int = 8765, data_dir: Optional[Path] = None, demo: bool = False) -> None:
    data_dir = data_dir or (ROOT / ".web_state")
    state = ServerState(data_dir=data_dir, demo_mode=demo)

    class BoundHandler(Handler):
        pass

    BoundHandler.state = state
    httpd = ThreadingHTTPServer(("127.0.0.1", port), BoundHandler)
    print(f"AgentCoach web UI running at http://127.0.0.1:{port}/")
    print(f"  data dir: {data_dir}")
    print(f"  demo mode: {demo}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        httpd.server_close()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=int(os.getenv("AGENTCOACH_PORT", "8765")))
    p.add_argument("--data-dir", type=str, default="")
    p.add_argument("--demo", action="store_true",
                   help="Force scripted coach + stub scoring; no LLM needed.")
    args = p.parse_args()
    serve(
        port=args.port,
        data_dir=Path(args.data_dir) if args.data_dir else None,
        demo=args.demo,
    )


if __name__ == "__main__":
    main()
