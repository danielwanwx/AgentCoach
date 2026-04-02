#!/usr/bin/env python3
"""Dynamic E2E: Learn SSE — fully dynamic conversation.

Both coach and user replies are LLM-generated. The user's reply is driven
by a "student persona" LLM that reads the coach's last message and responds
naturally according to the current phase of the learning arc.

Usage:
    python3 scripts/e2e_dynamic.py              # with voice
    python3 scripts/e2e_dynamic.py --no-voice   # text only
"""
from __future__ import annotations
import os, sys, re, subprocess, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
load_dotenv()

from agentcoach.llm.base import Message
from agentcoach.llm.openai_compat import OpenAICompatAdapter
from agentcoach.coach import Coach
from agentcoach.analytics.store import AnalyticsStore
from agentcoach.analytics.scorer import Scorer
from agentcoach.syllabus.loader import SyllabusLoader
from agentcoach.memory.store import CoachMemory
from agentcoach.kb.store import KnowledgeStore


# ── Voice ──────────────────────────────────────────────────────

def _clean(text):
    c = re.sub(r'[#*_`~\[\](){}|>]', '', text)
    c = re.sub(r'https?://\S+', '', c)
    c = re.sub(r'[\U0001f300-\U0001f9ff\u2705\u274c\u2611\u2610]', '', c)
    c = re.sub(r'<[^>]+>', '', c)
    c = re.sub(r'```[\s\S]*?```', '', c)
    c = re.sub(r'---+', '', c)
    c = re.sub(r'\|[^\n]+\|', '', c)
    c = re.sub(r'\n{2,}', '. ', c)
    c = re.sub(r'\n', ' ', c)
    return re.sub(r'\s{2,}', ' ', c).strip()


def _chunks(text, n=300):
    sents = re.split(r'(?<=[.!?])\s+', text)
    buf, out = "", []
    for s in sents:
        if len(buf) + len(s) + 1 <= n:
            buf = f"{buf} {s}".strip() if buf else s
        else:
            if buf: out.append(buf)
            buf = s[:n]
    if buf: out.append(buf)
    return out


def say_user(text, on):
    if not on: return
    for c in _chunks(_clean(text), 500):
        subprocess.run(["say", "-v", "Samantha", "-r", "175", "--", c], check=False)


def say_coach(text, tts, on):
    if not on: return
    clean = _clean(text)
    if tts == "say":
        # Fast mode: macOS say with Daniel (British male)
        for c in _chunks(clean, 500):
            subprocess.run(["say", "-v", "Daniel", "-r", "160", c], check=False)
    elif tts:
        # VibeVoice mode (high quality but slow)
        for c in _chunks(clean, 300)[:2]:
            try: tts.speak(c)
            except Exception as e: print(f"  [TTS err: {e}]")


# ── Student persona LLM ───────────────────────────────────────

# Each turn has a behavior directive that shapes what the student does,
# but the actual words come from the LLM reading the coach's real output.
TURN_DIRECTIVES = [
    # Turn 1: intro + say what you want to learn
    "Introduce yourself in one sentence. Say you want to learn about SSE and you've heard of WebSocket but aren't clear on the differences.",
    # Turn 2: ask a follow-up based on what coach just explained
    "Ask ONE specific follow-up question about something the coach just said that you want to understand deeper.",
    # Turn 3: ask another clarifying question, go deeper
    "Ask about a practical aspect — like when would you actually choose this in a real project, or how reconnection works.",
    # Turn 4: say you're ready to be quizzed
    "Say you feel like you understand the basics now and you're ready for the coach to quiz you.",
    # Turn 5: answer the quiz question (try to get it RIGHT)
    "Answer the coach's quiz question based on what you learned. Try to be correct and thorough.",
    # Turn 6: answer the next quiz question but get it WRONG
    "Answer the coach's question but DELIBERATELY get one detail wrong. Give a confident-sounding but incorrect answer.",
    # Turn 7: correct yourself after coach's feedback
    "Acknowledge your mistake based on what the coach just explained. Restate the correct answer in your own words.",
    # Turn 8: reflect and wrap up
    "Thank the coach. Say what you learned and what you still want to practice next time. Keep it brief.",
]

STUDENT_SYSTEM = """You are a software engineer student in a voice tutoring session.
You speak naturally in 1-3 short sentences. No markdown, no code, no formatting.
Sound like a real person: "hmm", "oh I see", "wait so...", "got it", "right right".
You are learning about SSE (Server-Sent Events) for the first time."""


def gen_student(llm, coach_said: str, turn: int) -> str:
    directive = TURN_DIRECTIVES[turn] if turn < len(TURN_DIRECTIVES) else "Wrap up the conversation naturally."
    msgs = [
        Message(role="system", content=STUDENT_SYSTEM),
        Message(role="user", content=(
            f"The coach just said:\n\n{coach_said}\n\n"
            f"Your behavior for this turn: {directive}\n\n"
            f"Reply as the student (1-3 sentences, natural speech):"
        )),
    ]
    return llm.generate(msgs)


# ── Main ───────────────────────────────────────────────────────

def main():
    voice_on = "--no-voice" not in sys.argv
    total_turns = len(TURN_DIRECTIVES)

    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "minimax")
    model_name = os.getenv("LLM_MODEL", "")
    if not api_key:
        print("Error: Set LLM_API_KEY"); sys.exit(1)

    if provider == "gemini":
        from agentcoach.llm.gemini import GeminiAdapter
        llm = GeminiAdapter(api_key=api_key, model=model_name or "gemini-2.0-flash")
    else:
        llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model_name)

    syllabus = SyllabusLoader()
    tmpdir = tempfile.mkdtemp()
    analytics = AnalyticsStore(db_path=os.path.join(tmpdir, "a.db"))
    mem = CoachMemory(db_path=os.path.join(tmpdir, "mem.db"))
    kb = KnowledgeStore(db_path=os.path.join(tmpdir, "kb.db"), use_vectors=False)

    # Seed KB
    kb.add_chunk(
        content="Server-Sent Events (SSE) is a server push technology enabling a client to receive automatic updates from a server via an HTTP connection. Unlike WebSocket which is bidirectional, SSE is unidirectional (server to client only). SSE uses a regular HTTP connection, making it simpler than WebSocket. It supports automatic reconnection, event IDs for resuming missed events, and is natively supported by browsers via the EventSource API. SSE is ideal for: live feeds, notifications, real-time dashboards, stock tickers. Limitations: unidirectional only, limited to text data (no binary), some browsers limit concurrent connections to ~6 per domain.",
        source="sse-guide", section="SSE Overview", category="system_design")
    kb.add_chunk(
        content="Comparison of real-time protocols: Polling — client repeatedly asks server, wasteful. Long Polling — client holds connection until data available, then reconnects. SSE — server pushes over one persistent HTTP connection, unidirectional, auto-reconnect with Last-Event-ID. WebSocket — full-duplex bidirectional, supports binary. Choose SSE when: server-to-client only, text data, want simplicity. Choose WebSocket when: bidirectional needed (chat, gaming), binary data required.",
        source="sse-guide", section="Protocol Comparison", category="system_design")
    kb.add_chunk(
        content="SSE reconnection: When connection drops, the browser automatically reconnects. If server sent event IDs, the browser includes Last-Event-ID header on reconnect. Server then sends only events after that ID, preventing duplicates. Requires server-side event buffering. Without proper server implementation, Last-Event-ID is useless. Retry interval controlled by server 'retry:' field.",
        source="sse-guide", section="Reconnection", category="system_design")
    print(f"  KB: {kb.get_stats()['total_chunks']} chunks")

    # TTS: --hq for VibeVoice (slow but best quality), default is macOS say (fast)
    tts = None
    if voice_on:
        if "--hq" in sys.argv:
            ref = "/tmp/karpathy_ref.wav" if os.path.exists("/tmp/karpathy_ref.wav") else None
            print("  Loading VibeVoice TTS (high quality, slower)...")
            from agentcoach.voice.tts import VibeVoiceTTS
            tts = VibeVoiceTTS(device="mps", cfg_scale=1.5, voice_sample=ref, lazy=True)
        else:
            print("  TTS: macOS say (fast) — use --hq for VibeVoice")
            tts = "say"

    # Build coach
    kb_results = kb.search("SSE server sent events polling websocket", limit=3)
    kb_teaching = "\n\n".join(r["content"][:600] for r in kb_results)

    voice_hint = ""
    if voice_on:
        voice_hint = ("\nCRITICAL: VOICE session. Max 3 sentences per response. "
                      "NO code, NO tables, NO markdown. Speak like a real conversation. "
                      "Teach one idea at a time. Wait for the student before moving on.")

    coach = Coach(
        llm=llm, mode="learn", kb_store=kb,
        topic_id="system_design.networking",
        topic_name="Server-Sent Events (SSE)",
        kb_teaching_context=kb_teaching,
        memory_context=voice_hint,
    )

    print()
    print("=" * 55)
    print("  LEARN SESSION: Server-Sent Events (SSE)")
    print(f"  Turns: {total_turns} (all replies LLM-generated)")
    if voice_on:
        print("  User=Samantha | Coach=VibeVoice")
    print("=" * 55)

    # ── Coach opening ──────────────────────────────────────────
    opening = coach.start()
    print(f"\n{'─'*55}")
    print(f"  🎓 Coach:\n  {opening}")
    print(f"{'─'*55}")
    say_coach(opening, tts, voice_on)

    last_coach = opening

    # ── Conversation loop ──────────────────────────────────────
    for turn in range(total_turns):
        time.sleep(0.3)

        # Generate student reply based on what coach actually said
        student = gen_student(llm, last_coach, turn)

        print(f"\n{'─'*55}")
        print(f"  🧑 You (turn {turn+1}/{total_turns}):\n  {student}")
        print(f"{'─'*55}")
        say_user(student, voice_on)

        time.sleep(0.2)

        # Coach responds
        response = coach.respond(student)
        last_coach = response

        qs = coach.quiz_state
        quiz = f"  [Q={qs.question_count} ✓={qs.correct_count} ✗={qs.incorrect_count}]" if qs.question_count > 0 else ""

        print(f"\n{'─'*55}")
        print(f"  🎓 Coach:\n  {response}")
        if quiz: print(quiz)
        print(f"{'─'*55}")
        say_coach(response, tts, voice_on)

    # ── Scoring ────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print("  SCORING")
    print(f"{'='*55}")

    qs = coach.quiz_state
    if qs.question_count > 0:
        weak = "; ".join(qs.weak_concepts[-5:]) if qs.weak_concepts else "none"
        mem.save_learning(
            f"Topic: SSE (system_design.networking) | Diff: {qs.difficulty} | "
            f"Score: {qs.correct_count}/{qs.question_count} | Weak: {weak}"
        )

    scorer = Scorer(llm, kb_store=kb, syllabus=syllabus)
    scores = scorer.score_session(coach.history, mode="learn", topic_id="system_design.networking")
    for s in scores:
        analytics.record_score("u1", s["topic_id"], s["score_delta"], "learn", s["evidence"])
        sign = "+" if s["score_delta"] > 0 else ""
        print(f"  {s['topic_id']}: {sign}{s['score_delta']} — {s['evidence']}")

    mastery = analytics.get_mastery("u1", "system_design.networking")
    print(f"\n  Mastery: {mastery}%")
    print(f"  History: {len(coach.history)} msgs")
    if any("[Previous conversation summary]" in getattr(m, 'content', '') for m in coach.history):
        print("  ✓ Compression happened")

    wrap = f"Done! SSE mastery is {mastery} percent."
    print(f"  🎓 {wrap}")
    say_coach(wrap, tts, voice_on)

    print(f"\n{'='*55}")
    print("  DONE")
    print(f"{'='*55}")

    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
