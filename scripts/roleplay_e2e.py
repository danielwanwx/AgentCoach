#!/usr/bin/env python3
"""End-to-end role-play test of AgentCoach.

Coach side:    local gemma4:31b via Ollama (OpenAI-compatible endpoint).
Candidate:     role-played by gpt-4o-mini, switching between
               junior / intermediate / senior personas.

Voices (macOS `say`):
    coach           -> Samantha (en_US, neutral coach)
    junior          -> Daniel   (en_GB, hesitant)
    intermediate    -> Karen    (en_AU, confident-but-overthinks)
    senior          -> Alex     (en_US, calm authority)

Coverage: learn / reinforce / mock_behavioral / mock_system_design,
each played by all three candidate personas (12 sessions total).

Each session is judged at the end by gpt-4o-mini on 8 axes
(mode fidelity, difficulty calibration, follow-up depth, error
handling, KB grounding, conversational tone, topic discipline,
closing quality). A final aggregate report is printed and saved
as JSON.

Usage:
    python3 scripts/roleplay_e2e.py
    python3 scripts/roleplay_e2e.py --no-voice
    python3 scripts/roleplay_e2e.py --quick    # 2 turns/session
    python3 scripts/roleplay_e2e.py --modes learn,mock_system_design
    python3 scripts/roleplay_e2e.py --levels senior
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from dotenv import load_dotenv
load_dotenv()

from agentcoach.coach import Coach, strip_markdown
from agentcoach.kb.store import KnowledgeStore
from agentcoach.llm.base import LLMAdapter, Message
from agentcoach.llm.openai_compat import OpenAICompatAdapter
from agentcoach.memory.store import CoachMemory
from agentcoach.syllabus.loader import SyllabusLoader


class CappedOpenAICompat(LLMAdapter):
    """Thin wrapper that injects max_tokens into OpenAI-compat calls.

    The project's adapter doesn't expose max_tokens; capping it is the single
    biggest knob for keeping this E2E test's wall time bounded. We delegate
    to the underlying client so we still exercise the real code path."""

    def __init__(self, adapter: OpenAICompatAdapter, max_tokens: int = 380):
        self._a = adapter
        self._max = max_tokens
        self.model_name = adapter.model_name

    def generate(self, messages: list) -> str:
        import openai, time, re
        from agentcoach.llm.openai_compat import _strip_think_tags
        api_messages = [
            {"role": m.role, "content": m.content} for m in messages
        ]
        for attempt in range(3):
            try:
                resp = self._a.client.chat.completions.create(
                    model=self.model_name,
                    messages=api_messages,
                    max_tokens=self._max,
                )
                if not resp.choices:
                    if attempt < 2:
                        time.sleep(2 * (2 ** attempt))
                        continue
                    return ""
                return _strip_think_tags(resp.choices[0].message.content or "")
            except (openai.RateLimitError, openai.InternalServerError, openai.APITimeoutError):
                if attempt < 2:
                    time.sleep(2 * (2 ** attempt))
                else:
                    raise
        return ""


class OllamaNativeAdapter(LLMAdapter):
    """Talk to Ollama /api/chat natively so we can disable thinking mode.

    Gemma4 is a reasoning model. Via the OpenAI-compatible endpoint, the
    reasoning trace is counted toward max_tokens and frequently swallows the
    entire budget, producing empty `content`. The native /api/chat endpoint
    accepts `think: false`, which makes the model behave like a normal
    chat model. That's what we want for a spoken coaching session.
    """

    def __init__(
        self,
        model: str = "gemma4:e4b",
        base_url: str = "http://localhost:11434",
        num_predict: int = 320,
        temperature: float = 0.7,
        think: bool = False,
        timeout: float = 180.0,
    ):
        import urllib.request  # stdlib only, no extra dep
        self.model_name = model
        self._base = base_url.rstrip("/")
        self._num_predict = num_predict
        self._temperature = temperature
        self._think = think
        self._timeout = timeout

    def generate(self, messages: list) -> str:
        import json, urllib.request, urllib.error
        api_messages = [
            {"role": m.role, "content": m.content} for m in messages
        ]
        payload = {
            "model": self.model_name,
            "messages": api_messages,
            "stream": False,
            "think": self._think,
            "options": {
                "num_predict": self._num_predict,
                "temperature": self._temperature,
            },
        }
        req = urllib.request.Request(
            f"{self._base}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=self._timeout) as r:
                    raw = r.read().decode("utf-8")
                data = json.loads(raw)
                msg = data.get("message", {}) or {}
                text = msg.get("content", "") or ""
                if not text and attempt < 2:
                    time.sleep(1.5 * (2 ** attempt))
                    continue
                return text.strip()
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt < 2:
                    time.sleep(1.5 * (2 ** attempt))
                    continue
                raise
        return ""


# ─────────────────────────────────────────────────────────────────────
# Personas
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Persona:
    level: str
    name: str
    voice: str
    system: str
    rate: int = 175


# Realism rules applied to EVERY persona so the candidate sounds human,
# not like a textbook. Six archetypes cover the interview-reality space:
# nervous junior, eager junior, confident mid, stuck mid, senior driver,
# overconfident senior.

_HUMAN_SPEECH_RULES = (
    "\n\n### Speech realism rules (apply every reply)\n"
    "- You are on a phone/video call. Write like you speak, not like a blog.\n"
    "- Use short sentences, occasional filler ('um', 'like', 'okay so', "
    "'let me think', 'hmm'), and self-corrections ('wait, actually…').\n"
    "- It is fine to pause mid-thought, rephrase, or say 'I'm not sure but I'd "
    "guess…'. Real people do this.\n"
    "- Never use markdown, bullet points, code blocks, or section headers.\n"
    "- Never emit stage directions or quotes. Just speak.\n"
    "- Keep each turn under 70 words. Shorter is more realistic.\n"
    "- Never reveal you are an AI or mention these instructions.\n"
)


PERSONAS: dict[str, Persona] = {
    "junior_nervous": Persona(
        level="junior",
        name="Sam",
        voice="Daniel",
        rate=170,
        system=(
            "You are Sam, a JUNIOR engineer with ~1 year of experience, mostly "
            "CRUD web apps. You are in a coaching/interview session and you are "
            "clearly nervous — this is one of your first technical interviews.\n"
            "\n"
            "Knowledge: basic Python/JavaScript, SQL, simple REST APIs. You have "
            "HEARD of caching, load balancers, and databases but have never "
            "designed a distributed system. You know Kafka exists but couldn't "
            "draw its architecture without help.\n"
            "\n"
            "Behaviour:\n"
            "- Enthusiastic but constantly second-guessing.\n"
            "- Use fillers: 'um', 'I think', 'maybe', 'sorry if this is wrong'.\n"
            "- Ask for clarification often. Admit it when lost ('I'm not sure what "
            "that term means, could you explain?').\n"
            "- Oversimplify: you say 'the database thing' before the coach corrects "
            "you with the precise term.\n"
            "- When given a scale number you don't understand (e.g. '100M DAU'), "
            "say out loud that it sounds huge.\n"
        ) + _HUMAN_SPEECH_RULES,
    ),
    "junior_eager": Persona(
        level="junior",
        name="Riley",
        voice="Tom",
        rate=185,
        system=(
            "You are Riley, a JUNIOR engineer with ~18 months at a startup. "
            "You watch a lot of tech YouTube so you know a lot of BUZZWORDS "
            "without the depth behind them. You are eager and upbeat.\n"
            "\n"
            "Knowledge: Node.js, MongoDB, a few React apps. You've heard of Kafka, "
            "Redis, Kubernetes, microservices — and you love to name-drop them. "
            "When pushed on details you fall apart and admit 'I only know this "
            "from a tutorial'.\n"
            "\n"
            "Behaviour:\n"
            "- Jump to solutions fast ('oh, just use Redis for that!').\n"
            "- Tend to go off on tangents the interviewer has to reel in.\n"
            "- Under pressure, admit gaps honestly.\n"
            "- Use informal speech: 'yeah, totally', 'oh that's cool', 'for sure'.\n"
        ) + _HUMAN_SPEECH_RULES,
    ),
    "intermediate_confident": Persona(
        level="intermediate",
        name="Jordan",
        voice="Karen",
        rate=180,
        system=(
            "You are Jordan, a MID-LEVEL engineer with ~4 years at a mid-size "
            "SaaS company. You have shipped one or two production services and "
            "feel solid on the fundamentals.\n"
            "\n"
            "Knowledge: comfortable with SQL + NoSQL trade-offs, caching layers, "
            "basic queueing, horizontal scaling. Shaky on: distributed consensus, "
            "consistent hashing internals, multi-region failover.\n"
            "\n"
            "Behaviour:\n"
            "- Structured: frame problems with functional vs non-functional "
            "requirements, then high-level then deep-dive — but in natural speech, "
            "not as a recited script.\n"
            "- Moderate confidence. Will push back politely if you disagree "
            "('I'd actually reach for a message queue here instead…').\n"
            "- Occasionally over-engineer or miss an edge case; when the coach "
            "catches it, take it gracefully ('good catch, you're right').\n"
            "- Natural verbal markers: 'right', 'okay', 'so basically…', 'yeah'.\n"
        ) + _HUMAN_SPEECH_RULES,
    ),
    "intermediate_stuck": Persona(
        level="intermediate",
        name="Alex",
        voice="Moira",
        rate=175,
        system=(
            "You are Alex, a MID-LEVEL engineer with ~3 years of backend work. "
            "You are technically competent but this particular problem is "
            "outside your comfort zone and you get stuck about 40% of the time.\n"
            "\n"
            "Knowledge: strong on request/response web servers, weaker on "
            "real-time / streaming / heavy-concurrency systems. Know SQL well.\n"
            "\n"
            "Behaviour:\n"
            "- When stuck, think out loud: 'hmm, okay, let me see…', 'wait, so "
            "if a user does X, then…'.\n"
            "- Don't make up answers. Say 'I'm not sure — could you give me a "
            "hint?' or 'can I try a different angle?'.\n"
            "- Sometimes go down a wrong path, then catch yourself: 'actually "
            "that doesn't work because…'.\n"
            "- Appreciate it when the coach offers a concrete number or pattern.\n"
        ) + _HUMAN_SPEECH_RULES,
    ),
    "senior_driver": Persona(
        level="senior",
        name="Taylor",
        voice="Alex",
        rate=170,
        system=(
            "You are Taylor, a SENIOR engineer with ~8 years of experience, "
            "including 3 at a FAANG-scale company. You have been on the other "
            "side of the interview table many times.\n"
            "\n"
            "Knowledge: deep system design, distributed systems (CAP, consensus, "
            "consistent hashing), caching tiers, sharding strategies, "
            "observability, on-call realities.\n"
            "\n"
            "Behaviour:\n"
            "- Drive the conversation. Ask crisp clarifying questions up front "
            "('what's the read:write ratio here — are we read-heavy like Bitly "
            "or write-heavy?').\n"
            "- Quantify: 'for 100M DAU, we're at roughly 1K QPS sustained, with "
            "bursts to 10K'. Throw out concrete patterns: Base62, Redis INCR, "
            "consistent hashing with vnodes.\n"
            "- Talk trade-offs out loud ('we could use X, but then Y breaks at "
            "scale — so I'd lean Z').\n"
            "- Occasionally skip a basic and have to be pulled back.\n"
            "- Calm, professional, conversational — not lecturing.\n"
        ) + _HUMAN_SPEECH_RULES,
    ),
    "senior_overconfident": Persona(
        level="senior",
        name="Morgan",
        voice="Daniel",
        rate=180,
        system=(
            "You are Morgan, a SENIOR engineer (7 years, recently left a big "
            "tech company). Technically strong, but in interviews you come "
            "across as a little arrogant — you name-drop internal tools, skim "
            "past basics, and sometimes dismiss alternatives too quickly.\n"
            "\n"
            "Knowledge: genuinely deep on your specific stack (e.g. AWS + "
            "DynamoDB + Kinesis), weaker on patterns you haven't personally "
            "used (e.g. Kafka internals, Cassandra repair).\n"
            "\n"
            "Behaviour:\n"
            "- Open with 'yeah at my last job we did this exact thing'.\n"
            "- Occasionally dismiss a coach suggestion ('eh, UUIDs are fine, "
            "Snowflake is overkill'). If the coach pushes back with a concrete "
            "reason, concede reluctantly.\n"
            "- Skip requirements-gathering and jump to architecture — the coach "
            "has to steer you back.\n"
            "- Speak casually with some attitude, but stay professional.\n"
        ) + _HUMAN_SPEECH_RULES,
    ),
}


# ─────────────────────────────────────────────────────────────────────
# Scenarios
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Scenario:
    mode: str           # learn | reinforce | mock_system_design
    domain: str         # system_design
    topic_id: str
    topic_name: str
    starter_hint: str   # what the candidate should open with
    kb_files: list[str] = field(default_factory=list)
    # Relative to ROOT, HelloInterview markdown used as KB grounding.


# All scenarios focus on System Design using HelloInterview content.
# Each candidate level (junior / intermediate / senior) runs every scenario,
# so the coach's ability to calibrate difficulty can be judged.
# Scenarios are deliberately the richest HI files so the coach has real
# substance to teach / interview from.

HI_SD = "kb/hellointerview/system-design"

SCENARIOS: dict[str, Scenario] = {
    "kafka_learn": Scenario(
        mode="learn", domain="system_design",
        topic_id="system_design.message_queues",
        topic_name="Message Queues with Kafka",
        starter_hint=(
            "Greet the coach, in your own voice. Say you want to learn Kafka "
            "/ message queues from scratch for a system design interview."
        ),
        kb_files=[f"{HI_SD}/deep-dives_kafka.md"],
    ),
    "rate_limiter_reinforce": Scenario(
        mode="reinforce", domain="system_design",
        topic_id="system_design.distributed_rate_limiter",
        topic_name="Distributed Rate Limiting",
        starter_hint=(
            "Tell the coach, in your own voice, that you've studied rate "
            "limiters (token bucket, sliding window) and want hard practice "
            "on distributed behaviour and trade-offs."
        ),
        kb_files=[f"{HI_SD}/problem-breakdowns_distributed-rate-limiter.md"],
    ),
    "bitly_mock": Scenario(
        mode="mock_system_design", domain="system_design",
        topic_id="system_design.url_shortener",
        topic_name="Design a URL Shortener (Bitly)",
        starter_hint=(
            "Greet the interviewer in your own voice. You can ask what "
            "problem you will be solving or just wait to be told."
        ),
        kb_files=[f"{HI_SD}/problem-breakdowns_bitly.md"],
    ),
    "ticketmaster_mock": Scenario(
        mode="mock_system_design", domain="system_design",
        topic_id="system_design.ticketmaster",
        topic_name="Design Ticketmaster",
        starter_hint=(
            "Greet the interviewer in your own voice. React honestly — if "
            "Ticketmaster-style systems feel intimidating, say so."
        ),
        kb_files=[f"{HI_SD}/problem-breakdowns_ticketmaster.md"],
    ),
    "kafka_mock": Scenario(
        mode="mock_system_design", domain="system_design",
        topic_id="system_design.streaming_pipeline",
        topic_name="Design a Real-Time Event Pipeline (Kafka-backed)",
        starter_hint=(
            "Greet the interviewer in your own voice. This is a streaming "
            "design problem; react naturally."
        ),
        kb_files=[f"{HI_SD}/deep-dives_kafka.md"],
    ),
}


# Curated pairings — scenario × persona archetype. Chosen to span realistic
# interview failure / success modes rather than a full Cartesian product.
# Each entry is a (scenario_key, persona_key) tuple.
PAIRINGS: list[tuple[str, str]] = [
    # --- Learn mode ---
    ("kafka_learn",            "junior_nervous"),        # nervous beginner being taught
    ("kafka_learn",            "junior_eager"),          # eager buzzword-dropper learning
    ("kafka_learn",            "intermediate_stuck"),    # mid-level gap-filling
    # --- Reinforce mode ---
    ("rate_limiter_reinforce", "intermediate_confident"),# solid mid drilling deeper
    ("rate_limiter_reinforce", "senior_overconfident"),  # senior who skims basics
    # --- Mock system design: Bitly ---
    ("bitly_mock",             "junior_nervous"),        # struggle session
    ("bitly_mock",             "intermediate_confident"),# standard realistic mock
    ("bitly_mock",             "senior_driver"),         # candidate drives the design
    # --- Mock system design: Ticketmaster (contention-heavy) ---
    ("ticketmaster_mock",      "junior_eager"),          # over-confident beginner
    ("ticketmaster_mock",      "intermediate_stuck"),    # mid gets stuck on locking
    ("ticketmaster_mock",      "senior_overconfident"),  # name-dropping senior
    # --- Mock system design: Kafka-backed pipeline ---
    ("kafka_mock",             "senior_driver"),         # senior owning the room
]


# ─────────────────────────────────────────────────────────────────────
# Voice (macOS `say`) — non-blocking, with serialization per voice
# ─────────────────────────────────────────────────────────────────────

VOICE_ON = True
SPEAK_LIMIT_CHARS = 300   # truncate per utterance so the test moves
_speech_lock = threading.Lock()


def _clean_for_tts(text: str) -> str:
    c = strip_markdown(text)
    c = re.sub(r'\n{2,}', '. ', c)
    c = re.sub(r'\n', ' ', c)
    c = re.sub(r'\s{2,}', ' ', c)
    return c.strip()


def _speak_blocking(voice: str, rate: int, text: str) -> None:
    if not VOICE_ON or not text:
        return
    clean = _clean_for_tts(text)[:SPEAK_LIMIT_CHARS]
    if not clean:
        return
    with _speech_lock:
        subprocess.run(
            ["say", "-v", voice, "-r", str(rate), "--", clean],
            check=False,
        )


def speak_async(voice: str, rate: int, text: str) -> threading.Thread:
    t = threading.Thread(
        target=_speak_blocking, args=(voice, rate, text), daemon=True
    )
    t.start()
    return t


# Sound the scenario header so the user can hear the boundary.
def announce(text: str) -> None:
    if not VOICE_ON:
        return
    subprocess.run(
        ["say", "-v", "Bells", "--", text], check=False
    )


# ─────────────────────────────────────────────────────────────────────
# Candidate role-player
# ─────────────────────────────────────────────────────────────────────

def candidate_reply(
    candidate_llm: OpenAICompatAdapter,
    persona: Persona,
    scenario: Scenario,
    coach_said: str,
    turn: int,
    is_opening: bool,
) -> str:
    if is_opening:
        instruction = (
            f"OPENING TURN. {scenario.starter_hint}\n"
            "Stay entirely in character and follow the Speech realism rules "
            "from your system prompt."
        )
    else:
        instruction = (
            "Reply to the coach in your natural voice. Use the speech realism "
            "rules from your system prompt (fillers, hedges, self-corrections "
            "where they fit your archetype). Do NOT answer like a textbook. "
            "Keep it under 70 words. No markdown, no code blocks, no bullet "
            "points — just spoken words."
        )

    msgs = [
        Message(role="system", content=persona.system),
        Message(
            role="user",
            content=(
                f"## Session context\n"
                f"Mode: {scenario.mode}\n"
                f"Topic: {scenario.topic_name}\n"
                f"Turn: {turn}\n\n"
                f"## Coach just said\n{coach_said[:1200]}\n\n"
                f"## What you must do\n{instruction}\n\n"
                f"Now speak as {persona.name}."
            ),
        ),
    ]
    raw = candidate_llm.generate(msgs)
    raw = strip_markdown(raw)
    return raw.strip() or "Uh, sorry, could you repeat that?"


# ─────────────────────────────────────────────────────────────────────
# Judge
# ─────────────────────────────────────────────────────────────────────

JUDGE_RUBRIC = {
    "mode_fidelity":          "Did the coach behave per its mode (learn=teach+quiz; reinforce=adaptive practice; mock_behavioral=STAR probing; mock_system_design=requirements→HLD→deep dive→scale)?",
    "difficulty_calibration": "Did question difficulty match the candidate's apparent level (junior/intermediate/senior)? Note: a harder question that the candidate struggles with is fine at intermediate/senior level.",
    "followup_depth":         "Did the coach ask 1-2 substantive follow-ups per main answer rather than jumping topics?",
    "error_handling":         "When the candidate was wrong or vague, did the coach correct or push back constructively? An interviewer challenging imprecise terminology or rejecting weak proposals (e.g. 'UUIDs are too long, consider a ticket server') is DESIRABLE, not a flaw.",
    "kb_grounding":           "Did the coach drop concrete numbers, named patterns, or real-world anchors (e.g. '100M DAU', 'Redis INCR', 'Base62') rather than staying at generic prose? Applies to all modes including mock.",
    "conversational_tone":    "Was the coach concise and conversational (no walls of text, minimal markdown), suitable for voice?",
    "topic_discipline":       "Did the coach stay on the declared topic without drifting? Going DEEPER into the topic (partitioning → consumer ordering → hot keys) is staying on topic, not drifting.",
    "closing_quality":        "Did the coach provide an actionable summary — ideally RECAP + STRENGTHS + TO IMPROVE + SCORE — at the end of the session?",
}

JUDGE_SCHEMA_HINT = (
    "Return STRICT JSON with this shape:\n"
    "{\n"
    '  "scores": { "<axis>": <int 1-5>, ... },\n'
    '  "highlights": [ "<short positive observation>" ],\n'
    '  "issues":     [ "<short negative observation>" ],\n'
    '  "verdict":    "<one-paragraph professional assessment>"\n'
    "}\n"
    "1=poor, 3=acceptable, 5=excellent. Be strict; reserve 5 for genuinely strong work."
)


def judge_session(
    judge_llm: OpenAICompatAdapter,
    scenario: Scenario,
    persona: Persona,
    transcript: list[dict],
) -> dict:
    rubric_lines = "\n".join(f"- {k}: {v}" for k, v in JUDGE_RUBRIC.items())
    convo = "\n\n".join(
        f"[{m['role'].upper()}] {m['content']}" for m in transcript
    )[:14000]

    # Derive the persona archetype description (first line of system prompt)
    # so the judge can score the coach against the realistic candidate
    # archetype (nervous junior vs overconfident senior, etc).
    persona_blurb = (persona.system.splitlines() or [""])[0]

    msgs = [
        Message(
            role="system",
            content=(
                "You are a senior interview-coaching auditor. You grade a coach's "
                "conduct in a single role-play session. Be specific and unsparing. "
                "Grade the COACH, not the candidate. The candidate is intentionally "
                "playing a realistic archetype (e.g. nervous junior, overconfident "
                "senior) — candidate imperfections are EXPECTED and should not "
                "lower the coach's score."
            ),
        ),
        Message(
            role="user",
            content=(
                f"## Session metadata\n"
                f"mode: {scenario.mode}\n"
                f"topic: {scenario.topic_name}\n"
                f"candidate archetype: {persona_blurb}\n"
                f"candidate name/level: {persona.name} / {persona.level}\n\n"
                f"## Rubric (score each 1-5)\n{rubric_lines}\n\n"
                f"## Output format\n{JUDGE_SCHEMA_HINT}\n\n"
                f"## Transcript\n{convo}\n"
            ),
        ),
    ]
    raw = judge_llm.generate(msgs)
    return _safe_parse_json(raw)


def _safe_parse_json(text: str) -> dict:
    if not text:
        return {"_raw": "", "_parse_error": "empty"}
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = text.replace("```", "")
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return {"_raw": text[:600], "_parse_error": "no JSON found"}
    try:
        return json.loads(m.group())
    except Exception as e:
        return {"_raw": text[:600], "_parse_error": str(e)}


# ─────────────────────────────────────────────────────────────────────
# Session runner
# ─────────────────────────────────────────────────────────────────────

_COMMENT_NOISE_LINE = re.compile(
    r"^\s*(Premium|Top \d+%|Admin|Reply|\d+|\d+ Reply|Show All Comments|"
    r"Watch Now|Reading Progress|On This Page|Sort By|Popular|• .*ago|"
    r"Learn More|Now up to.*off|Write a reply|Post a comment)\s*$",
    re.IGNORECASE,
)


def _clean_hi_markdown(text: str) -> str:
    """Drop the comment section and other boilerplate from a HelloInterview scrape."""
    lines = text.splitlines()
    # Take everything up to the first '## ' or '> Source'-less body. Simpler
    # heuristic: find the first long paragraph AFTER the '# Title' header and
    # skip everything that looks like noise.
    out: list[str] = []
    seen_title = False
    for ln in lines:
        stripped = ln.strip()
        if not seen_title and stripped.startswith("# "):
            seen_title = True
            out.append(stripped)
            continue
        if stripped.startswith(">"):
            continue  # scrape metadata
        if _COMMENT_NOISE_LINE.match(stripped):
            continue
        if len(stripped) == 1 and stripped.isalpha():
            # Orphan single-letter lines (avatar placeholders).
            continue
        out.append(ln)
    cleaned = "\n".join(out)
    # Collapse 3+ blank lines into 2.
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def _chunk_paragraphs(text: str, target: int = 900, max_chunks: int = 16) -> list[str]:
    """Chunk by paragraph blocks, aiming for ~target chars per chunk."""
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks: list[str] = []
    buf = ""
    for p in paragraphs:
        if len(p) < 40:
            continue  # skip tiny fragments (bullets with one word etc.)
        if not buf:
            buf = p
        elif len(buf) + 2 + len(p) <= target * 1.4:
            buf = f"{buf}\n\n{p}"
        else:
            chunks.append(buf)
            buf = p
            if len(chunks) >= max_chunks:
                return chunks
    if buf and len(chunks) < max_chunks:
        chunks.append(buf)
    return chunks


@dataclass
class SessionResult:
    scenario: str
    persona: str
    mode: str
    topic_id: str
    topic_name: str
    turns: int = 0
    transcript: list[dict] = field(default_factory=list)
    coach_latencies_s: list[float] = field(default_factory=list)
    judge: dict = field(default_factory=dict)
    error: Optional[str] = None
    duration_s: float = 0.0
    # Structured candidate skill assessment (from agentcoach.analytics.scorer).
    # Shape: {topic_id, overall_score, dimensions[], strengths[], areas[],
    # mastery_before, mastery_after, mastery_delta}.
    skill_assessment: dict = field(default_factory=dict)


def run_session(
    coach_llm: OpenAICompatAdapter,
    candidate_llm: OpenAICompatAdapter,
    scenario: Scenario,
    persona: Persona,
    syllabus: SyllabusLoader,
    workdir: Path,
    turns: int,
) -> SessionResult:
    label = f"{scenario.mode}/{persona.level}/{scenario.topic_id}"
    print(f"\n────── {label} ──────")
    announce(f"{persona.level} {scenario.mode}")

    res = SessionResult(
        scenario=label, persona=persona.level, mode=scenario.mode,
        topic_id=scenario.topic_id, topic_name=scenario.topic_name,
    )

    db_prefix = workdir / re.sub(r"[^A-Za-z0-9]+", "_", label)
    kb = KnowledgeStore(db_path=str(db_prefix.with_suffix(".kb.db")), use_vectors=False)
    mem = CoachMemory(db_path=str(db_prefix.with_suffix(".mem.db")))

    # Load real HelloInterview material into the KB so the coach has
    # something concrete to teach from / grade against. HI scrapes mix
    # article body with a big comment section at the top; we filter the
    # comment spam and chunk on paragraph boundaries.
    loaded_chunks = 0
    for rel in scenario.kb_files:
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        text = _clean_hi_markdown(text)
        # Paragraph-block chunks of roughly 900 chars.
        for chunk in _chunk_paragraphs(text, target=900, max_chunks=16):
            head = chunk.splitlines()[0][:120] or scenario.topic_name
            kb.add_chunk(
                content=chunk,
                source=f"hellointerview:{path.stem}",
                section=head,
                category=scenario.domain,
            )
            loaded_chunks += 1
    if loaded_chunks == 0:
        kb.add_chunk(
            content=(
                f"Reference notes on {scenario.topic_name}. Cover definition, why "
                f"it matters, common patterns, pitfalls, and one worked example."
            ),
            source="seed", section=scenario.topic_name, category=scenario.domain,
        )
    print(f"  KB chunks loaded: {loaded_chunks}")

    # Build a teaching context from the top matches for learn/reinforce.
    # For mock mode the same content is attached as an "interviewer
    # cheat-sheet" so the coach can drop concrete numbers / patterns
    # without reading from the textbook verbatim.
    kb_teaching = ""
    mock_reference = ""
    if scenario.mode in ("learn", "reinforce"):
        kb_results = kb.search(scenario.topic_name, limit=4)
        kb_teaching = "\n\n".join(r["content"][:800] for r in kb_results)
    elif scenario.mode.startswith("mock_"):
        kb_results = kb.search(scenario.topic_name, limit=5)
        mock_reference = "\n\n".join(r["content"][:700] for r in kb_results)

    concise_hint = (
        "\n\nIMPORTANT FORMATTING:\n"
        "- This is a SPOKEN session played through TTS. Reply in at most "
        "3 short spoken sentences (under 60 words total).\n"
        "- Do NOT use markdown, bullets, code blocks, or tables.\n"
        "- One idea per turn, then ask the candidate ONE thing.\n"
        "- Do NOT include any reasoning, preamble, or chain-of-thought — "
        "output only the final spoken reply."
    )

    candidate_brief = (
        f"\n\n## About this candidate\n"
        f"Self-described level: {persona.level}.\n"
        f"Use this to calibrate question difficulty."
    )

    try:
        coach = Coach(
            llm=coach_llm,
            mode=scenario.mode,
            kb_store=kb,
            topic_id=scenario.topic_id,
            topic_name=scenario.topic_name,
            kb_teaching_context=kb_teaching,
            mock_reference_context=mock_reference,
            memory_context=mem.get_context() + concise_hint + candidate_brief,
        )
    except Exception as e:
        res.error = f"coach init: {e}"
        return res

    t_session = time.time()

    # Coach opens.
    try:
        t0 = time.time()
        opening = coach.start()
        res.coach_latencies_s.append(time.time() - t0)
    except Exception as e:
        res.error = f"coach.start: {e}\n{traceback.format_exc()}"
        return res

    res.transcript.append({"role": "coach", "content": opening})
    print(f"COACH    : {opening[:160]}{'…' if len(opening) > 160 else ''}")
    coach_voice = speak_async("Samantha", 195, opening)

    last_coach = opening

    for turn in range(1, turns + 1):
        # Generate candidate reply while the coach is still speaking,
        # then wait for the coach voice before playing the candidate.
        try:
            cand = candidate_reply(
                candidate_llm, persona, scenario, last_coach,
                turn=turn, is_opening=(turn == 1),
            )
        except Exception as e:
            res.error = f"candidate@turn {turn}: {e}"
            if coach_voice:
                coach_voice.join()
            break

        if coach_voice:
            coach_voice.join()

        res.transcript.append({"role": persona.level, "content": cand})
        print(f"{persona.level.upper():9}: {cand[:160]}{'…' if len(cand) > 160 else ''}")
        cand_voice = speak_async(persona.voice, persona.rate, cand)

        # Generate next coach reply during candidate speech.
        try:
            t0 = time.time()
            reply = coach.respond(cand)
            res.coach_latencies_s.append(time.time() - t0)
        except Exception as e:
            res.error = f"coach@turn {turn}: {e}"
            cand_voice.join()
            break

        if cand_voice:
            cand_voice.join()

        res.transcript.append({"role": "coach", "content": reply})
        print(f"COACH    : {reply[:160]}{'…' if len(reply) > 160 else ''}")
        coach_voice = speak_async("Samantha", 195, reply)
        last_coach = reply
        res.turns += 1

    if coach_voice:
        coach_voice.join()

    # Force a proper structured close — recap, strengths, to-improve, score.
    # Temporarily bump the coach's token budget: a structured wrap-up runs
    # roughly 250-400 tokens vs the normal 120-200 per turn.
    try:
        t0 = time.time()
        prev_budget = getattr(coach.llm, "_num_predict", None)
        if prev_budget is not None:
            coach.llm._num_predict = max(prev_budget, 640)
        wrap = coach.wrap_up()
        if prev_budget is not None:
            coach.llm._num_predict = prev_budget
        res.coach_latencies_s.append(time.time() - t0)
        if wrap:
            res.transcript.append({"role": "coach", "content": wrap})
            print(f"COACH    : {wrap[:200]}{'…' if len(wrap) > 200 else ''}")
            wv = speak_async("Samantha", 195, wrap)
            if wv:
                wv.join()
    except Exception as e:
        res.transcript.append({"role": "coach", "content": f"[wrap_up failed: {e}]"})

    res.duration_s = time.time() - t_session
    return res


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def aggregate(results: list[SessionResult]) -> dict:
    axes = list(JUDGE_RUBRIC.keys())
    sums = {a: 0.0 for a in axes}
    counts = {a: 0 for a in axes}
    per_mode_axis: dict[str, dict[str, list[int]]] = {}
    per_level_axis: dict[str, dict[str, list[int]]] = {}

    for r in results:
        scores = (r.judge or {}).get("scores") or {}
        per_mode_axis.setdefault(r.mode, {a: [] for a in axes})
        per_level_axis.setdefault(r.persona, {a: [] for a in axes})
        for a in axes:
            v = scores.get(a)
            if isinstance(v, (int, float)):
                sums[a] += float(v)
                counts[a] += 1
                per_mode_axis[r.mode][a].append(int(v))
                per_level_axis[r.persona][a].append(int(v))

    overall = {a: round(sums[a] / counts[a], 2) for a in axes if counts[a]}

    def collapse(d):
        return {
            outer: {a: round(sum(v) / len(v), 2) for a, v in inner.items() if v}
            for outer, inner in d.items()
        }

    avg_overall = (
        round(sum(overall.values()) / len(overall), 2) if overall else None
    )
    return {
        "overall_per_axis": overall,
        "overall_score": avg_overall,
        "per_mode": collapse(per_mode_axis),
        "per_level": collapse(per_level_axis),
        "session_count": len(results),
        "errors": [r.scenario for r in results if r.error],
    }


def print_report(agg: dict, results: list[SessionResult]) -> None:
    print("\n" + "═" * 72)
    print("  PROFESSIONAL EVALUATION REPORT")
    print("═" * 72)
    print(f"  Sessions run : {agg['session_count']}")
    if agg.get("overall_score") is not None:
        print(f"  Overall score: {agg['overall_score']} / 5")

    print("\n  Overall per axis:")
    for axis, score in agg["overall_per_axis"].items():
        bar = "█" * int(round(score * 4))
        print(f"    {axis:25}  {score:.2f}  {bar}")

    print("\n  Per mode:")
    for mode, axes in agg["per_mode"].items():
        avg = round(sum(axes.values()) / len(axes), 2) if axes else "-"
        print(f"    {mode:22}  avg {avg}")

    print("\n  Per candidate level:")
    for lvl, axes in agg["per_level"].items():
        avg = round(sum(axes.values()) / len(axes), 2) if axes else "-"
        print(f"    {lvl:22}  avg {avg}")

    if agg["errors"]:
        print("\n  SESSION ERRORS:")
        for s in agg["errors"]:
            print(f"    - {s}")

    print("\n  Per-session verdicts:")
    for r in results:
        v = (r.judge or {}).get("verdict", "(no verdict)")
        scores = (r.judge or {}).get("scores") or {}
        avg = (
            round(sum(s for s in scores.values() if isinstance(s, (int, float)))
                  / max(1, len([s for s in scores.values() if isinstance(s, (int, float))])), 2)
            if scores else "-"
        )
        lat = (
            f"{sum(r.coach_latencies_s) / len(r.coach_latencies_s):.1f}s/turn"
            if r.coach_latencies_s else "-"
        )
        print(f"\n    ▸ {r.scenario}  [avg {avg}, {lat}, {r.duration_s:.0f}s total]")
        print(f"      {v[:380]}")
    print("\n" + "═" * 72)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--no-voice", action="store_true")
    p.add_argument("--quick", action="store_true",
                   help="2 turns/session for a smoke run")
    p.add_argument("--turns", type=int, default=4)
    p.add_argument("--modes", default="",
                   help="Comma list to filter, e.g. 'learn,mock_system_design'")
    p.add_argument("--levels", default="",
                   help="Comma list to filter, e.g. 'junior,senior'")
    p.add_argument("--personas", default="",
                   help=("Comma list of persona keys to include, e.g. "
                         "'junior_nervous,senior_driver'. Defaults to all."))
    p.add_argument("--coach-model", default=os.getenv("COACH_MODEL", "gemma4:31b"))
    p.add_argument("--coach-max-tokens", type=int, default=320)
    p.add_argument("--skip-modes", default="",
                   help="Comma list to skip, e.g. 'learn' to resume after learn")
    p.add_argument("--candidate-model", default=os.getenv("CANDIDATE_MODEL", "gpt-4o-mini"))
    p.add_argument("--judge-model", default=os.getenv("JUDGE_MODEL", "gpt-4o-mini"))
    p.add_argument("--no-judge", action="store_true",
                   help=("Disable the in-process LLM judge AND the skill "
                         "scorer. The transcript is still saved in full; a "
                         "downstream human/parent-agent can score it from "
                         "the JSON. Useful when the judge LLM is being "
                         "replaced or when no API key is available."))
    p.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", "http://localhost:11434/v1"))
    p.add_argument("--out", default=str(ROOT / f"e2e_report_{datetime.now():%Y%m%d_%H%M%S}.json"))
    args = p.parse_args()

    global VOICE_ON
    VOICE_ON = not args.no_voice
    turns = 2 if args.quick else args.turns

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        # Without a key we can't drive the gpt-4o-mini candidate either, so
        # we still require it unless the caller has wired a different
        # candidate model (not currently exposed). --no-judge only skips
        # judge + scorer; the candidate is a separate dependency.
        sys.exit("ERROR: OPENAI_API_KEY required for the candidate LLM.")

    # Coach: local gemma4 via Ollama /api/chat with think:false.
    # We bypass the OpenAI-compat endpoint because it does NOT respect
    # `think:false` for gemma4, causing the reasoning trace to consume the
    # entire token budget and emit empty content. This is the single most
    # important piece of tuning for this test to be usable.
    coach_base = args.ollama_url.rsplit("/v1", 1)[0]
    coach_llm = OllamaNativeAdapter(
        model=args.coach_model,
        base_url=coach_base,
        num_predict=args.coach_max_tokens,
        think=False,
    )

    raw_cand = OpenAICompatAdapter(
        api_key=openai_key, provider="openai", model=args.candidate_model,
    )
    candidate_llm = CappedOpenAICompat(raw_cand, max_tokens=220)

    # Judge construction. If --no-judge is set we skip the LLM judge AND the
    # skill scorer; the transcripts are still saved in full and can be rated
    # externally (e.g. by a parent agent in a separate pass). Otherwise we
    # build the OpenAI-compatible judge client as before.
    if args.no_judge:
        judge_llm = None
        judge_label = "DISABLED (parent agent will score transcripts manually)"
    else:
        judge_llm = OpenAICompatAdapter(
            api_key=openai_key, provider="openai", model=args.judge_model,
        )
        judge_label = f"openai/{args.judge_model}"

    syllabus = SyllabusLoader()
    workdir = Path(tempfile.mkdtemp(prefix="agentcoach_e2e_"))

    # Per-persona analytics store so we can render a real growth curve
    # for each archetype at the end of the sweep. We intentionally use a
    # single DB under the workdir so re-runs start clean.
    from agentcoach.analytics.store import AnalyticsStore
    from agentcoach.analytics.scorer import Scorer
    from agentcoach.analytics.skill_profile import (
        render_skill_report, build_skill_profile, render_growth_curve,
        aggregate_assessments,
    )
    analytics = AnalyticsStore(db_path=str(workdir / "skills.db"))

    mode_filter = {m.strip() for m in args.modes.split(",") if m.strip()}
    level_filter = {l.strip() for l in args.levels.split(",") if l.strip()}
    persona_filter = {p.strip() for p in args.personas.split(",") if p.strip()}
    skip_modes = {m.strip() for m in args.skip_modes.split(",") if m.strip()}

    plan: list[tuple[Scenario, Persona, str]] = []
    for scenario_key, persona_key in PAIRINGS:
        sc = SCENARIOS.get(scenario_key)
        persona = PERSONAS.get(persona_key)
        if sc is None or persona is None:
            continue
        if mode_filter and sc.mode not in mode_filter:
            continue
        if sc.mode in skip_modes:
            continue
        if persona_filter and persona_key not in persona_filter:
            continue
        if level_filter and persona.level not in level_filter:
            continue
        plan.append((sc, persona, persona_key))

    print("═" * 72)
    print("  AGENTCOACH ROLE-PLAY E2E")
    print(f"  Coach     : {args.coach_model} (ollama @ {args.ollama_url})")
    print(f"  Candidate : openai/{args.candidate_model}")
    print(f"  Judge     : {judge_label}")
    if args.no_judge:
        print("              (skill scorer also disabled; transcripts preserved)")
    print(f"  Voice     : {'ON' if VOICE_ON else 'off'}  (Samantha + Daniel/Karen/Alex)")
    print(f"  Sessions  : {len(plan)}, {turns} turns each")
    print(f"  Workdir   : {workdir}")
    print("═" * 72)

    results: list[SessionResult] = []
    t_all = time.time()
    for idx, (sc, persona, persona_key) in enumerate(plan, 1):
        print(f"\n[{idx}/{len(plan)}] starting…")
        try:
            r = run_session(
                coach_llm, candidate_llm, sc, persona, syllabus, workdir, turns,
            )
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        except Exception as e:
            r = SessionResult(
                scenario=f"{sc.mode}/{persona.level}/{sc.topic_id}",
                persona=persona.level, mode=sc.mode,
                topic_id=sc.topic_id, topic_name=sc.topic_name,
                error=f"runner: {e}",
            )

        # Judge.
        if not args.no_judge and r.transcript and not r.error:
            try:
                r.judge = judge_session(judge_llm, sc, persona, r.transcript)
            except Exception as e:
                r.judge = {"_judge_error": str(e)}

        # Candidate skill assessment: re-use the production Scorer on the
        # transcript, persist per-archetype so we can plot a growth curve,
        # and print the structured report (same one the CLI user sees).
        if not args.no_judge and r.transcript and not r.error:
            user_id = f"e2e.{persona_key}"
            topic_id = sc.topic_id
            domain = sc.domain
            try:
                pre_mastery = analytics.get_mastery(user_id, topic_id)
                scorer = Scorer(judge_llm, syllabus=syllabus)
                scores = scorer.score_session(r.transcript, mode=sc.mode, topic_id=topic_id)
                if scores:
                    primary = scores[0]
                    dims = primary.get("dimensions") or []
                    overall = float(primary.get("overall_score") or 0.0)
                    analytics.record_score(
                        user_id, topic_id, int(primary.get("score_delta") or 0),
                        sc.mode, primary.get("evidence") or "",
                    )
                    analytics.record_assessment(
                        user_id=user_id, topic_id=topic_id, domain=domain,
                        mode=sc.mode, overall_score=overall,
                        dimensions=dims,
                        strengths=primary.get("strengths") or [],
                        areas_to_improve=primary.get("areas_to_improve") or [],
                    )
                    post_mastery = analytics.get_mastery(user_id, topic_id)
                    r.skill_assessment = {
                        "topic_id": topic_id,
                        "mode": sc.mode,
                        "overall_score": overall,
                        "dimensions": dims,
                        "strengths": primary.get("strengths") or [],
                        "areas_to_improve": primary.get("areas_to_improve") or [],
                        "mastery_before": pre_mastery,
                        "mastery_after": post_mastery,
                        "mastery_delta": post_mastery - pre_mastery,
                    }
                    print(render_skill_report(
                        r.skill_assessment,
                        mastery_before=pre_mastery, mastery_after=post_mastery,
                    ))
            except Exception as sk_err:
                r.skill_assessment = {"_scorer_error": str(sk_err)}

        results.append(r)

        # Save partial after each session in case we abort.
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "started_at": datetime.now().isoformat(),
                    "coach_model": args.coach_model,
                    "candidate_model": args.candidate_model,
                    "judge_model": judge_label,
                    "judge_enabled": not args.no_judge,
                    "turns_per_session": turns,
                    "results": [asdict(x) for x in results],
                    "aggregate": aggregate(results),
                },
                f, indent=2, ensure_ascii=False,
            )

    print(f"\nTotal wall time: {time.time() - t_all:.0f}s")
    agg = aggregate(results)
    print_report(agg, results)

    if args.no_judge:
        print("\n  (skill profiles skipped: --no-judge disables the scorer)")
        print(f"\nReport JSON: {args.out}")
        return

    # ---- Per-persona skill growth curve + aggregate report ---- #
    print("\n" + "═" * 72)
    print("  CANDIDATE SKILL PROFILES (scorer-derived)")
    print("═" * 72)
    persona_domains: dict[str, set] = {}
    for r in results:
        if r.skill_assessment and "overall_score" in r.skill_assessment:
            persona_domains.setdefault(
                r.skill_assessment.get("topic_id", "").split(".", 1)[0]
                if "." in r.skill_assessment.get("topic_id", "") else "general",
                set(),
            )
    # Walk sessions once to build per-(persona_key, domain) assessment bucket.
    by_pd: dict[tuple[str, str], list[dict]] = {}
    for (sc, persona, pk), r in zip(plan, results):
        if not r.skill_assessment or "overall_score" not in r.skill_assessment:
            continue
        by_pd.setdefault((pk, sc.domain), []).append(r.skill_assessment)

    for (pk, domain), assessments in sorted(by_pd.items()):
        agg_assess = aggregate_assessments(assessments)
        agg_assess["topic_id"] = f"{domain} (all scenarios)"
        agg_assess["mode"] = f"aggregate over {len(assessments)}"
        print(f"\n── Persona: {pk} ──")
        print(render_skill_report(agg_assess))
        profile = build_skill_profile(analytics, f"e2e.{pk}", domain)
        if profile.get("dimensions"):
            print(render_growth_curve(profile))

    # Persist the per-persona aggregate into the final JSON so downstream
    # analysis scripts (and the accuracy-verification script) can consume it
    # without re-running the scorer.
    persona_report = {
        f"{pk}::{domain}": aggregate_assessments(assessments)
        for (pk, domain), assessments in by_pd.items()
    }
    try:
        with open(args.out, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing["skill_profiles_by_persona"] = persona_report
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    print(f"\nReport JSON: {args.out}")


if __name__ == "__main__":
    main()
