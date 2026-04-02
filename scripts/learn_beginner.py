#!/usr/bin/env python3
"""Learn mode E2E: Complete beginner learns System Design interview flow.

Candidate persona: SDE with 2 years of coding experience, never prepped for
system design interviews. Doesn't know the framework, vocabulary, or what
interviewers expect. Genuinely confused, asks naive questions, gets things
wrong, gradually builds understanding.

Usage:
    python3 scripts/learn_beginner.py           # with voice (fast)
    python3 scripts/learn_beginner.py --hq      # with VibeVoice
    python3 scripts/learn_beginner.py --no-voice
"""
from __future__ import annotations
import os, sys, re, subprocess, tempfile, time, json

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


def say_student(text, on):
    if not on: return
    for c in _chunks(_clean(text), 500):
        subprocess.run(["say", "-v", "Samantha", "-r", "170", "--", c], check=False)


def say_coach(text, tts, on):
    if not on: return
    clean = _clean(text)
    if tts == "say":
        for c in _chunks(clean, 500):
            subprocess.run(["say", "-v", "Daniel", "-r", "155", "--", c], check=False)
    elif tts:
        for c in _chunks(clean, 300)[:2]:
            try: tts.speak(c)
            except: pass


# ── Beginner student persona ──────────────────────────────────

STUDENT_SYSTEM = """You are a software developer with 2 years of experience writing backend code.
You've NEVER prepared for a system design interview before. You know how to code but:
- You don't know the "system design interview framework"
- Terms like "sharding", "consistent hashing", "CAP theorem" are things you've vaguely heard but can't explain
- You've never designed anything beyond a single-server CRUD app
- You're nervous and honest about what you don't know

Behavior rules:
- Speak naturally in 2-4 sentences. This is a voice conversation.
- Show genuine confusion: "Wait, I'm not sure I follow..." / "Hmm, what do you mean by..."
- Ask naive questions that a real beginner would ask
- When the coach explains something, sometimes paraphrase it back WRONG to test your understanding
- Sometimes say "oh!" when something clicks
- Admit when you're lost: "Honestly I have no idea" / "I've never thought about that"
- NO markdown, NO code, NO lists. Pure natural speech.
- Be curious and engaged, not passive."""

TURN_BEHAVIORS = [
    # T1: Total beginner intro
    "Introduce yourself. Say you're nervous because you have a system design interview next week and you've never done one before. Ask the coach what system design interviews even are.",
    # T2: Confused about scope
    "The coach is explaining the interview format. Ask a naive question like 'But how am I supposed to design a whole system in 45 minutes? I can barely finish a coding problem in that time.'",
    # T3: Try to understand the framework
    "The coach explained a framework or steps. Try to paraphrase it back but get one part slightly wrong or out of order. Show you're trying.",
    # T4: Panic about vocabulary
    "The coach mentioned some technical terms. Admit you don't know what one of them means. Ask for a simple explanation. Be honest.",
    # T5: Starting to get it
    "Something is clicking. Say 'oh!' and explain what you think you understand. But ask if you're right because you're not confident.",
    # T6: Ask a practical question
    "Ask something practical like 'So when the interviewer asks me to design Twitter, where do I literally start? Like what's the first thing I say?'",
    # T7: Attempt to apply the framework
    "Try to walk through the first few steps of designing a simple system (like a URL shortener) using what the coach taught. Make it messy and incomplete — you're a beginner.",
    # T8: Get feedback, ask for help on weak spot
    "The coach gave feedback on your attempt. Acknowledge what you messed up and ask for specific help on the part you're weakest on.",
    # T9: Second attempt after coaching
    "Try again on the weak spot the coach helped with. Do better this time but still not perfect.",
    # T10: Wrap up with honest self-assessment
    "Thank the coach. Give an honest assessment of where you are — what makes sense now and what you still need to practice. Ask what you should study before your interview next week.",
]


def gen_student(llm, coach_said: str, turn: int, conversation_summary: str) -> str:
    behavior = TURN_BEHAVIORS[turn] if turn < len(TURN_BEHAVIORS) else "Wrap up."
    msgs = [
        Message(role="system", content=STUDENT_SYSTEM),
        Message(role="user", content=(
            f"Conversation so far: {conversation_summary}\n\n"
            f"The coach just said:\n{coach_said}\n\n"
            f"Your behavior: {behavior}\n\n"
            f"Reply as the student (2-4 sentences, natural nervous speech):"
        )),
    ]
    return llm.generate(msgs)


# ── KB ─────────────────────────────────────────────────────────

def load_kb(kb):
    for doc_id in ["#ccdec4", "#f1b14c"]:
        result = subprocess.run(["qmd", "get", doc_id, "--full"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            sections = re.split(r'\n(?=#{1,3} )', result.stdout.strip())
            for sec in sections:
                lines = sec.strip().split('\n')
                title = lines[0].lstrip('#').strip() if lines else ""
                body = re.sub(r'<[^>]+>', '', '\n'.join(lines[1:]).strip())
                if len(body) > 80:
                    kb.add_chunk(content=body[:1000], source="sd-books",
                                 section=title, category="system_design")
    # System design interview framework
    kb.add_chunk(
        content="System design interview framework: Step 1 — Understand the problem and establish design scope. Ask clarifying questions about scale, features, users, constraints. Step 2 — Propose high-level design. Draw the main components: clients, load balancer, web servers, databases, caches, message queues. Step 3 — Design deep dive. Pick 2-3 components and go into detail on data model, API design, scaling approach. Step 4 — Wrap up. Discuss trade-offs, bottlenecks, monitoring, future improvements. The whole interview is 35-45 minutes.",
        source="sd-framework", section="Interview Framework", category="system_design")
    kb.add_chunk(
        content="Common beginner mistakes in system design interviews: jumping straight to solution without asking requirements, overcomplicating the design with buzzwords you can't explain, not discussing trade-offs, ignoring scale numbers, drawing boxes without explaining data flow, not considering failure modes. The interviewer wants to see your thought process, not a perfect answer.",
        source="sd-framework", section="Common Mistakes", category="system_design")
    print(f"  KB: {kb.get_stats()['total_chunks']} chunks")


# ── Main ───────────────────────────────────────────────────────

def main():
    voice_on = "--no-voice" not in sys.argv
    hq = "--hq" in sys.argv
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

    tts = None
    if voice_on:
        if hq:
            ref = "/tmp/karpathy_ref.wav" if os.path.exists("/tmp/karpathy_ref.wav") else None
            print("  Loading VibeVoice TTS...")
            from agentcoach.voice.tts import VibeVoiceTTS
            tts = VibeVoiceTTS(device="mps", cfg_scale=1.5, voice_sample=ref, lazy=True)
        else:
            print("  TTS: macOS say (fast)")
            tts = "say"

    # Student profile
    mem.save_profile("Junior SDE, 2 years experience, never done system design interview. Knows Python, basic SQL, has built CRUD apps. Nervous about upcoming interview.")

    # KB teaching content
    kb_results = kb.search("system design interview framework steps", limit=5)
    kb_teaching = "\n\n".join(r["content"][:600] for r in kb_results)

    voice_hint = ("\nCRITICAL: This is a CONVERSATIONAL tutoring session with a COMPLETE BEGINNER."
                  "\nMax 4 sentences per response. NO code blocks, NO tables, NO long lists."
                  "\nSpeak like a patient, encouraging tutor. Use simple analogies."
                  "\nCheck understanding frequently. Ask if they have questions."
                  "\nThis student has NEVER done a system design interview. Start from absolute basics."
                  "\nTeach ONE concept at a time, then wait for their response before moving on.")

    coach = Coach(
        llm=llm, mode="learn", kb_store=kb,
        topic_id="system_design.core_concepts",
        topic_name="System Design Interview Framework",
        kb_teaching_context=kb_teaching,
        memory_context=mem.get_context() + voice_hint,
    )

    print()
    print("=" * 55)
    print("  LEARN: System Design Interview (Complete Beginner)")
    print(f"  Turns: {total_turns}")
    if voice_on:
        print(f"  Student=Samantha | Coach={'VibeVoice' if hq else 'Daniel'}")
    print("=" * 55)

    # Coach opening
    opening = coach.start()
    print(f"\n{'─'*55}")
    print(f"  🎓 Coach:\n  {opening}")
    print(f"{'─'*55}")
    say_coach(opening, tts, voice_on)

    last_coach = opening
    summary = "Beginner learning system design interview basics from scratch."

    # Conversation loop
    for turn in range(total_turns):
        time.sleep(0.3)

        student = gen_student(llm, last_coach, turn, summary)

        print(f"\n{'─'*55}")
        print(f"  🧑 Student (turn {turn+1}/{total_turns}):\n  {student}")
        print(f"{'─'*55}")
        say_student(student, voice_on)

        summary += f"\nStudent: {student[:120]}"
        time.sleep(0.2)

        response = coach.respond(student)
        last_coach = response
        summary += f"\nCoach: {response[:120]}"

        qs = coach.quiz_state
        quiz = f"  [Q={qs.question_count} ✓={qs.correct_count} ✗={qs.incorrect_count}]" if qs.question_count > 0 else ""

        print(f"\n{'─'*55}")
        print(f"  🎓 Coach:\n  {response}")
        if quiz: print(quiz)
        print(f"{'─'*55}")
        say_coach(response, tts, voice_on)

    # Session end
    print(f"\n{'='*55}")
    print("  SESSION END")
    print(f"{'='*55}")

    # Save learning state
    qs = coach.quiz_state
    if qs.question_count > 0:
        weak = "; ".join(qs.weak_concepts[-5:]) if qs.weak_concepts else "none"
        mem.save_learning(
            f"Topic: SD Interview Framework | Diff: {qs.difficulty} | "
            f"Score: {qs.correct_count}/{qs.question_count} | Weak: {weak}"
        )

    # Score
    scorer = Scorer(llm, kb_store=kb, syllabus=syllabus)
    scores = scorer.score_session(coach.history, mode="learn", topic_id="system_design.core_concepts")
    for s in scores:
        analytics.record_score("beginner", s["topic_id"], s["score_delta"], "learn", s["evidence"])
        sign = "+" if s["score_delta"] > 0 else ""
        print(f"  {s['topic_id']}: {sign}{s['score_delta']} — {s['evidence']}")

    mastery = analytics.get_mastery("beginner", "system_design.core_concepts")
    print(f"\n  Mastery: {mastery}%")

    # Save transcript
    mem.save_transcript("beginner", "system_design.core_concepts",
                        "System Design Interview Framework", "learn",
                        coach.history, scores)
    print("  Transcript saved.")

    # Verify transcript
    ts = mem.get_transcripts("beginner")
    if ts:
        t = ts[0]
        print(f"  Transcript: {len(t['transcript'])} messages, {t['timestamp']}")

    print(f"  History: {len(coach.history)} msgs")

    wrap = f"Session done. Mastery {mastery} percent."
    print(f"\n  🎓 {wrap}")
    say_coach(wrap, tts, voice_on)

    print(f"\n{'='*55}")
    print("  DONE")
    print(f"{'='*55}")

    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
