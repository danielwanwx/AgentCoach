#!/usr/bin/env python3
"""Mock Interview E2E: System Design — Design a Notification System

Real scenario: Coach is the interviewer, LLM-generated candidate answers.
The candidate (Javi) has real experience but makes realistic mistakes.

Coach: VibeVoice 1.5B (interviewer voice)
Candidate: macOS say Samantha (candidate voice)

Usage:
    python3 scripts/mock_interview.py           # with voice
    python3 scripts/mock_interview.py --fast    # macOS say for both (fast)
    python3 scripts/mock_interview.py --no-voice
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


def _chunks(text, n=400):
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


def _safe_say(voice, rate, text):
    """Run say with -- to prevent text being parsed as flags."""
    subprocess.run(["say", "-v", voice, "-r", str(rate), "--", text], check=False)


def say_candidate(text, on):
    if not on: return
    for c in _chunks(_clean(text), 500):
        _safe_say("Samantha", 170, c)


def say_interviewer(text, tts, on):
    if not on: return
    clean = _clean(text)
    if tts == "say":
        for c in _chunks(clean, 500):
            _safe_say("Daniel", 155, c)
    elif tts:
        for c in _chunks(clean, 300)[:2]:
            try: tts.speak(c)
            except Exception as e: print(f"  [TTS err: {e}]")


# ── Candidate persona ─────────────────────────────────────────

CANDIDATE_SYSTEM = """You are Javi, a software engineer with 3 years of experience, interviewing for a senior backend/system design role. You have real experience building distributed systems at a mid-size startup.

Behavior rules:
- Answer in 3-6 sentences, like you're speaking in a real interview. Natural, not scripted.
- Show your thinking process: "So first I'd think about... then..." / "One approach would be..."
- You're good but not perfect:
  - You know the basics well (load balancers, databases, caching)
  - You sometimes forget edge cases until prompted
  - You occasionally use slightly wrong terminology then self-correct
  - You ask clarifying questions when appropriate (like a real candidate)
- Show personality: "That's a good question" / "Hmm let me think about that" / "Actually wait"
- If the interviewer pushes back, don't cave immediately — defend your choice, then acknowledge valid points
- NO markdown, NO code blocks, NO bullet points. Pure speech."""

TURN_BEHAVIORS = [
    # Turn 1: Clarifying requirements
    "The interviewer just gave you a design problem. Ask 2-3 clarifying questions about scale, features, and constraints. Be specific.",
    # Turn 2: High-level architecture
    "Propose a high-level architecture. Name the main components and how they connect. Keep it concise but show breadth.",
    # Turn 3: Deep dive on a component
    "The interviewer asked about a specific component. Explain your design choice in detail. Show you've thought about tradeoffs.",
    # Turn 4: Handle a pushback
    "The interviewer challenged your approach. Defend your choice first, then acknowledge the valid concern and propose a mitigation.",
    # Turn 5: Scalability
    "Explain how your system handles scale. Talk about specific numbers if you can. Mention what breaks first.",
    # Turn 6: Data storage choice
    "The interviewer asked about your database/storage choice. Justify it with read/write patterns and data characteristics.",
    # Turn 7: Failure handling
    "Discuss what happens when a component fails. Be specific about failure modes and recovery. Mention at least one thing you'd monitor.",
    # Turn 8: Get something slightly wrong
    "Answer the interviewer's question but get one technical detail slightly wrong. Sound confident about it. This is realistic.",
    # Turn 9: Correct after feedback
    "The interviewer pointed out your mistake. Acknowledge it gracefully, explain what you confused it with, give the correct answer.",
    # Turn 10: Wrap up
    "The interviewer asks if you have questions. Ask one thoughtful question about their actual system, then briefly summarize your design.",
]


def gen_candidate(llm, interviewer_said: str, turn: int, history_summary: str) -> str:
    behavior = TURN_BEHAVIORS[turn] if turn < len(TURN_BEHAVIORS) else "Wrap up naturally."
    msgs = [
        Message(role="system", content=CANDIDATE_SYSTEM),
        Message(role="user", content=(
            f"Interview context so far: {history_summary}\n\n"
            f"The interviewer just said:\n{interviewer_said}\n\n"
            f"Your behavior this turn: {behavior}\n\n"
            f"Reply as Javi (3-6 sentences, natural speech):"
        )),
    ]
    return llm.generate(msgs)


# ── KB ─────────────────────────────────────────────────────────

def load_kb(kb):
    # Load real system design content from qmd
    for doc_id in ["#ccdec4", "#f1b14c"]:  # cache.md, chat-system ch12
        result = subprocess.run(["qmd", "get", doc_id, "--full"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            sections = re.split(r'\n(?=#{1,3} )', result.stdout.strip())
            for sec in sections:
                lines = sec.strip().split('\n')
                title = lines[0].lstrip('#').strip() if lines else ""
                body = re.sub(r'<[^>]+>', '', '\n'.join(lines[1:]).strip())
                if len(body) > 80:
                    kb.add_chunk(content=body[:1000], source="system-design-books",
                                 section=title, category="system_design")

    # Add notification-specific content
    kb.add_chunk(
        content="Push notification system design: Components include notification service, message queue (Kafka/RabbitMQ), device token registry, provider adapters (APNs for iOS, FCM for Android), rate limiter, and analytics pipeline. Key decisions: pull vs push model, notification priority levels, batching for efficiency, retry with exponential backoff for failed deliveries, user preference storage for opt-in/opt-out.",
        source="notification-design", section="Push Notifications", category="system_design")
    kb.add_chunk(
        content="Notification delivery guarantees: At-least-once delivery is standard (exactly-once is impractical). Deduplication via idempotency keys. Fan-out patterns: on-write (eager, write to each user's queue) vs on-read (lazy, compute at read time). For celebrity problem with millions of followers, use hybrid: eager for normal users, lazy for high-follower accounts. Message ordering: per-user FIFO via partition key in Kafka.",
        source="notification-design", section="Delivery Guarantees", category="system_design")

    stats = kb.get_stats()
    print(f"  KB: {stats['total_chunks']} chunks")


# ── Main ───────────────────────────────────────────────────────

def main():
    voice_on = "--no-voice" not in sys.argv
    fast_mode = "--fast" in sys.argv
    total_turns = 10

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

    print("Setting up...")
    load_kb(kb)

    # TTS setup
    tts = None
    if voice_on:
        if fast_mode:
            print("  TTS: macOS say (fast mode)")
            tts = "say"
        else:
            ref = "/tmp/karpathy_ref.wav" if os.path.exists("/tmp/karpathy_ref.wav") else None
            print("  Loading VibeVoice TTS (interviewer voice)...")
            from agentcoach.voice.tts import VibeVoiceTTS
            tts = VibeVoiceTTS(device="mps", cfg_scale=1.5, voice_sample=ref, lazy=True)

    # Candidate profile
    mem.save_profile("Javi, 3 years backend experience, built distributed event pipeline at startup, familiar with Kafka, Redis, PostgreSQL, AWS. Transitioning to senior role.")

    # Coach as system design interviewer
    voice_hint = ""
    if voice_on:
        voice_hint = ("\nCRITICAL: VOICE interview. Max 4 sentences per response. "
                      "NO code, NO tables, NO markdown. Speak like a real interviewer. "
                      "Ask ONE question at a time. Be conversational. Push the candidate to go deeper.")

    coach = Coach(
        llm=llm, mode="mock_system_design", kb_store=kb,
        topic_id="system_design.message_queues",
        topic_name="Design a Notification System",
        memory_context=mem.get_context() + voice_hint,
    )

    print()
    print("=" * 55)
    print("  MOCK INTERVIEW: Design a Notification System")
    print(f"  Turns: {total_turns}")
    if voice_on:
        mode_label = "Daniel (fast)" if fast_mode else "VibeVoice (HQ)"
        print(f"  Candidate=Samantha | Interviewer={mode_label}")
    print("=" * 55)

    # ── Interviewer opening ────────────────────────────────────
    opening = coach.start()
    print(f"\n{'─'*55}")
    print(f"  🎤 Interviewer:\n  {opening}")
    print(f"{'─'*55}")
    say_interviewer(opening, tts, voice_on)

    last_interviewer = opening
    conversation_summary = "System design interview: Design a Notification System."

    # ── Interview loop ─────────────────────────────────────────
    for turn in range(total_turns):
        time.sleep(0.3)

        # Generate candidate answer based on what interviewer actually said
        candidate = gen_candidate(llm, last_interviewer, turn, conversation_summary)

        print(f"\n{'─'*55}")
        print(f"  🧑 Javi (turn {turn+1}/{total_turns}):\n  {candidate}")
        print(f"{'─'*55}")
        say_candidate(candidate, voice_on)

        # Update summary for context
        conversation_summary += f"\nCandidate: {candidate[:150]}"

        time.sleep(0.2)

        # Interviewer responds
        response = coach.respond(candidate)
        last_interviewer = response
        conversation_summary += f"\nInterviewer: {response[:150]}"

        print(f"\n{'─'*55}")
        print(f"  🎤 Interviewer:\n  {response}")
        print(f"{'─'*55}")
        say_interviewer(response, tts, voice_on)

    # ── Scoring ────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print("  INTERVIEW SCORING")
    print(f"{'='*55}")

    scorer = Scorer(llm, kb_store=kb, syllabus=syllabus)
    scores = scorer.score_session(coach.history, mode="mock", topic_id="system_design.message_queues")
    total_delta = 0
    for s in scores:
        analytics.record_score("javi", s["topic_id"], s["score_delta"], "mock", s["evidence"])
        sign = "+" if s["score_delta"] > 0 else ""
        print(f"  {s['topic_id']}: {sign}{s['score_delta']} — {s['evidence']}")
        total_delta += s["score_delta"]

    mastery = analytics.get_mastery("javi", "system_design.message_queues")
    print(f"\n  Total delta: {'+' if total_delta > 0 else ''}{total_delta}")
    print(f"  Message Queues mastery: {mastery}%")
    print(f"  History: {len(coach.history)} msgs")

    wrap = f"Interview complete. Score delta {total_delta}. Mastery now {mastery} percent."
    print(f"\n  🎤 {wrap}")
    say_interviewer(wrap, tts, voice_on)

    print(f"\n{'='*55}")
    print("  DONE")
    print(f"{'='*55}")

    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
