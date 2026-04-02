#!/usr/bin/env python3
"""Comprehensive E2E test: all modes × all domains × all personas.

Runs multiple test scenarios with voice output, evaluates each, logs issues.
Coach (MiniMax LLM) + Student (LLM-generated replies).

Usage:
    python3 scripts/comprehensive_e2e.py              # with voice
    python3 scripts/comprehensive_e2e.py --no-voice   # text only
"""
from __future__ import annotations
import os, sys, re, subprocess, tempfile, time, json, traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
load_dotenv()

from agentcoach.llm.base import Message
from agentcoach.llm.openai_compat import OpenAICompatAdapter
from agentcoach.coach import Coach
from agentcoach.analytics.store import AnalyticsStore
from agentcoach.analytics.scorer import Scorer
from agentcoach.analytics.recommender import Recommender
from agentcoach.syllabus.loader import SyllabusLoader
from agentcoach.memory.store import CoachMemory
from agentcoach.kb.store import KnowledgeStore


# ── Personas ───────────────────────────────────────────────────

PERSONAS = {
    "beginner": {
        "name": "Alex",
        "system": "You are Alex, a complete beginner. You've NEVER studied system design, algorithms, or AI. "
                  "You know basic Python. You're confused by technical terms. Ask naive questions. "
                  "Admit when lost: 'I have no idea what that means'. 2-3 sentences max.",
    },
    "junior": {
        "name": "Sam",
        "system": "You are Sam, a junior SDE with 1 year experience. You know basics but have gaps. "
                  "You've built CRUD apps. You sometimes use wrong terminology. "
                  "Try to answer but get 40% of details wrong. 2-4 sentences.",
    },
    "mid": {
        "name": "Jordan",
        "system": "You are Jordan, mid-level engineer (3 years). Transitioning to senior. "
                  "Solid fundamentals, sometimes overthinks. Asks good follow-up questions. "
                  "Gets 70% right but misses edge cases. 3-4 sentences.",
    },
    "senior": {
        "name": "Taylor",
        "system": "You are Taylor, senior engineer returning after 2 year break. "
                  "Deep knowledge but rusty on specifics. Remembers concepts, forgets details. "
                  "Sometimes says 'I used to know this...' Confident but occasionally wrong. 3-4 sentences.",
    },
    "non_cs": {
        "name": "Morgan",
        "system": "You are Morgan, a product manager who wants to understand technical concepts. "
                  "No CS degree. Asks 'why does this matter?' and 'explain like I'm five'. "
                  "Good at analogies but doesn't know implementation details. 2-3 sentences.",
    },
}

# ── Scenarios ──────────────────────────────────────────────────

SCENARIOS = [
    # Learn mode - different domains + personas
    # Learn mode - 4 domains × different personas
    {"mode": "learn", "domain": "system_design", "topic_id": "system_design.caching",
     "topic_name": "Caching", "persona": "beginner", "turns": 12},
    {"mode": "learn", "domain": "ai_agent", "topic_id": "ai_agent.rag",
     "topic_name": "RAG", "persona": "non_cs", "turns": 12},
    {"mode": "learn", "domain": "algorithms", "topic_id": "algorithms.binary_search",
     "topic_name": "Binary Search", "persona": "junior", "turns": 10},
    {"mode": "learn", "domain": "behavioral", "topic_id": "behavioral.star_framework",
     "topic_name": "STAR Framework", "persona": "mid", "turns": 10},

    # Reinforce mode - 2 domains
    {"mode": "reinforce", "domain": "system_design", "topic_id": "system_design.caching",
     "topic_name": "Caching", "persona": "mid", "turns": 10},
    {"mode": "reinforce", "domain": "ai_agent", "topic_id": "ai_agent.transformer",
     "topic_name": "Transformer Architecture", "persona": "senior", "turns": 10},

    # Mock mode - 4 domains × different personas
    {"mode": "mock", "domain": "system_design", "topic_id": "system_design.url_shortener",
     "topic_name": "Design URL Shortener", "persona": "mid", "turns": 12},
    {"mode": "mock", "domain": "ai_agent", "topic_id": "ai_agent.agent_architecture",
     "topic_name": "Agent Architecture", "persona": "junior", "turns": 10},
    {"mode": "mock", "domain": "behavioral", "topic_id": "behavioral.leadership",
     "topic_name": "Leadership", "persona": "senior", "turns": 10},
    {"mode": "mock", "domain": "algorithms", "topic_id": "algorithms.dynamic_programming",
     "topic_name": "Dynamic Programming", "persona": "beginner", "turns": 10},
]

# Turn behaviors per mode
LEARN_BEHAVIORS = [
    "Introduce yourself briefly. Say what you want to learn.",
    "Ask a follow-up question about what the coach just explained.",
    "Try to paraphrase what you learned but get a detail slightly wrong.",
    "Ask a practical question about when/how to use this.",
    "Say you're ready for the quiz.",
    "Answer the quiz question (try to be correct based on what you learned).",
    "Answer the next question but get one detail wrong deliberately.",
    "Correct yourself after feedback. Reflect on what you learned.",
]

REINFORCE_BEHAVIORS = [
    "Say you've studied this before but need practice. Ask to start.",
    "Answer the first question confidently.",
    "Answer but miss an edge case.",
    "Ask about a tricky scenario you're unsure about.",
    "Try to explain the tradeoffs in your own words.",
    "Answer a harder question, show depth but not perfection.",
    "Admit what you're still shaky on.",
    "Summarize what you've solidified vs what needs more work.",
]

MOCK_BEHAVIORS = [
    "Ask 2-3 clarifying questions about the design problem.",
    "Propose a high-level architecture with main components.",
    "Dive deeper on a specific component the interviewer asked about.",
    "Defend your design choice when the interviewer pushes back.",
    "Discuss how the system handles scale.",
    "Explain your database/storage choice.",
    "Discuss failure modes and monitoring.",
    "Get a technical detail slightly wrong (realistic mistake).",
    "Correct yourself after interviewer feedback.",
    "Wrap up. Ask the interviewer a thoughtful question.",
]


def get_behaviors(mode):
    if mode == "learn": return LEARN_BEHAVIORS
    if mode == "reinforce": return REINFORCE_BEHAVIORS
    return MOCK_BEHAVIORS


# ── Voice ──────────────────────────────────────────────────────

VOICE_ON = "--no-voice" not in sys.argv


def _clean_tts(text):
    c = re.sub(r'[#*_`~\[\](){}|>]', '', text)
    c = re.sub(r'https?://\S+', '', c)
    c = re.sub(r'```[\s\S]*?```', '', c)
    c = re.sub(r'---+', '', c)
    c = re.sub(r'\|[^\n]+\|', '', c)
    c = re.sub(r'\n{2,}', '. ', c)
    c = re.sub(r'\n', ' ', c)
    return re.sub(r'\s{2,}', ' ', c).strip()


def _tts_chunks(text, n=500):
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


def say_student(text):
    if not VOICE_ON: return
    for c in _tts_chunks(_clean_tts(text), 500)[:2]:
        subprocess.run(["say", "-v", "Samantha", "-r", "175", "--", c], check=False)


def say_coach(text):
    if not VOICE_ON: return
    for c in _tts_chunks(_clean_tts(text), 500)[:2]:
        subprocess.run(["say", "-v", "Daniel", "-r", "155", "--", c], check=False)


# ── Student LLM ────────────────────────────────────────────────

def gen_student(llm, persona: dict, coach_said: str, turn: int, behaviors: list, topic: str) -> str:
    behavior = behaviors[turn % len(behaviors)]
    msgs = [
        Message(role="system", content=persona["system"]),
        Message(role="user", content=(
            f"Topic: {topic}\n"
            f"Coach just said:\n{coach_said[:500]}\n\n"
            f"Behavior: {behavior}\n\n"
            f"Reply as {persona['name']} (natural speech, 2-4 sentences):"
        )),
    ]
    return llm.generate(msgs)


# ── Issue tracker ──────────────────────────────────────────────

class IssueTracker:
    def __init__(self):
        self.issues = []

    def add(self, scenario: str, category: str, severity: str, description: str):
        self.issues.append({
            "scenario": scenario,
            "category": category,
            "severity": severity,
            "description": description,
            "timestamp": datetime.now().isoformat(),
        })

    def summary(self):
        by_severity = {}
        by_category = {}
        for i in self.issues:
            by_severity[i["severity"]] = by_severity.get(i["severity"], 0) + 1
            by_category[i["category"]] = by_category.get(i["category"], 0) + 1
        return {"total": len(self.issues), "by_severity": by_severity, "by_category": by_category}


# ── Run one scenario ───────────────────────────────────────────

def run_scenario(llm, scenario: dict, syllabus, tmpdir: str, tracker: IssueTracker, quick: bool):
    mode = scenario["mode"]
    topic_id = scenario["topic_id"]
    topic_name = scenario["topic_name"]
    persona = PERSONAS[scenario["persona"]]
    turns = 3 if quick else scenario["turns"]
    behaviors = get_behaviors(mode)

    label = f"{mode}/{scenario['domain']}/{scenario['persona']}"
    print(f"\n  Running: {label} ({topic_name}, {turns} turns)")

    analytics = AnalyticsStore(db_path=os.path.join(tmpdir, f"{label.replace('/', '_')}_analytics.db"))
    mem = CoachMemory(db_path=os.path.join(tmpdir, f"{label.replace('/', '_')}_mem.db"))
    kb = KnowledgeStore(db_path=os.path.join(tmpdir, f"{label.replace('/', '_')}_kb.db"), use_vectors=False)

    # Seed minimal KB
    kb.add_chunk(content=f"Teaching content for {topic_name}. This is a placeholder for KB content.",
                 source="test", section=topic_name, category=scenario["domain"])

    # Pre-record prereqs if needed for reinforce/mock
    if mode in ("reinforce", "mock"):
        topic = syllabus.get_topic(topic_id)
        if topic:
            for prereq in topic.get("prerequisites", []):
                analytics.record_score("test_user", prereq, 50, "mock")
            analytics.record_score("test_user", topic_id, 30, "learn")

    # Map mode to prompt template
    if mode == "mock":
        prompt_mode = f"mock_{scenario['domain']}"
    else:
        prompt_mode = mode

    # Build coach
    kb_results = kb.search(topic_name, limit=3)
    kb_teaching = "\n\n".join(r["content"][:400] for r in kb_results) if mode == "learn" else ""

    concise_hint = ("\nKeep responses to 3-5 sentences max. Be conversational. "
                    "NO code blocks, NO tables. Teach one concept at a time.")

    try:
        coach = Coach(
            llm=llm, mode=prompt_mode, kb_store=kb,
            topic_id=topic_id, topic_name=topic_name,
            kb_teaching_context=kb_teaching,
            memory_context=mem.get_context() + concise_hint,
        )
    except Exception as e:
        tracker.add(label, "init", "critical", f"Coach init failed: {e}")
        return None

    # Run conversation
    results = {"label": label, "turns": [], "errors": []}

    try:
        opening = coach.start()
        results["opening_len"] = len(opening)
        if len(opening) > 2000:
            tracker.add(label, "verbosity", "medium", f"Opening too long: {len(opening)} chars")
        print(f"    🎓 Coach: {opening[:120]}...")
        say_coach(opening)
    except Exception as e:
        tracker.add(label, "coach_start", "critical", f"Coach.start() failed: {e}")
        return results

    last_coach = opening

    for turn in range(turns):
        try:
            # Generate student reply
            student = gen_student(llm, persona, last_coach, turn, behaviors, topic_name)
            if not student or len(student.strip()) < 5:
                tracker.add(label, "student_gen", "medium", f"Empty student reply at turn {turn+1}")
                student = "Can you explain that again?"

            print(f"    🧑 {persona['name']} ({turn+1}/{turns}): {student[:100]}...")
            say_student(student)

            # Coach responds
            response = coach.respond(student)
            if not response or len(response.strip()) < 5:
                tracker.add(label, "coach_respond", "high", f"Empty coach response at turn {turn+1}")
                continue

            print(f"    🎓 Coach: {response[:120]}...")
            say_coach(response)

            results["turns"].append({
                "turn": turn + 1,
                "student_len": len(student),
                "coach_len": len(response),
            })

            # Check verbosity
            if len(response) > 2000:
                tracker.add(label, "verbosity", "low", f"Turn {turn+1}: coach response {len(response)} chars")

            last_coach = response

        except Exception as e:
            tracker.add(label, "conversation", "high", f"Turn {turn+1} error: {e}")
            results["errors"].append(str(e))

    # Check QuizState
    qs = coach.quiz_state
    results["quiz_state"] = {
        "active": qs._quiz_active,
        "questions": qs.question_count,
        "correct": qs.correct_count,
        "incorrect": qs.incorrect_count,
        "difficulty": qs.difficulty,
    }

    if mode == "learn" and qs._quiz_active and qs.question_count == 0:
        tracker.add(label, "quiz_state", "medium", "Quiz activated but 0 questions tracked")

    # Check compression
    results["history_len"] = len(coach.history)
    compressed = any("[Previous conversation summary]" in getattr(m, 'content', '') for m in coach.history)
    results["compressed"] = compressed
    if len(coach.history) > 14 and not compressed:
        tracker.add(label, "compression", "medium", f"History {len(coach.history)} msgs but not compressed")

    # Score
    try:
        scorer = Scorer(llm, kb_store=kb, syllabus=syllabus)
        scores = scorer.score_session(coach.history, mode=mode, topic_id=topic_id)
        results["scores"] = scores

        if not scores:
            tracker.add(label, "scoring", "high", "Scorer returned no scores")
        else:
            for s in scores:
                analytics.record_score("test_user", s["topic_id"], s["score_delta"], mode, s["evidence"])
                # Check topic normalization
                if not syllabus.get_topic(s["topic_id"]):
                    tracker.add(label, "topic_norm", "high",
                                f"Score topic '{s['topic_id']}' not in syllabus (normalization failed)")

        mastery = analytics.get_mastery("test_user", topic_id)
        results["mastery"] = mastery
        if scores and mastery == 0:
            tracker.add(label, "mastery", "high", f"Scores recorded but mastery still 0%")

    except Exception as e:
        tracker.add(label, "scoring", "critical", f"Scoring failed: {e}")
        results["scores"] = []

    # Save transcript
    try:
        mem.save_transcript("test_user", topic_id, topic_name, mode, coach.history, scores)
        ts = mem.get_transcripts("test_user")
        if not ts:
            tracker.add(label, "transcript", "high", "Transcript save succeeded but get_transcripts empty")
        results["transcript_saved"] = True
    except Exception as e:
        tracker.add(label, "transcript", "high", f"Transcript save failed: {e}")
        results["transcript_saved"] = False

    # Save learning state
    if qs.question_count > 0:
        weak = "; ".join(qs.weak_concepts[-3:]) if qs.weak_concepts else "none"
        mem.save_learning(f"Topic: {topic_name} | Diff: {qs.difficulty} | Score: {qs.correct_count}/{qs.question_count} | Weak: {weak}")

    # Check recommender
    try:
        rec = Recommender(analytics)
        topics = [t for t in syllabus.get_topics(scenario["domain"]) if t.get("resources")]
        if topics:
            recommendation = rec.recommend("test_user", topics, syllabus=syllabus)
            results["recommendation"] = recommendation
    except Exception as e:
        tracker.add(label, "recommender", "high", f"Recommender failed: {e}")

    print(f"    ✓ {len(results.get('turns', []))} turns, mastery={results.get('mastery', '?')}%, "
          f"scores={len(results.get('scores', []))}, quiz={qs.question_count}Q")

    return results


# ── Main ───────────────────────────────────────────────────────

def main():
    quick = "--quick" in sys.argv

    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "minimax")
    model_name = os.getenv("LLM_MODEL", "")
    if not api_key:
        print("Error: Set LLM_API_KEY"); sys.exit(1)

    llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model_name)
    syllabus = SyllabusLoader()
    tracker = IssueTracker()
    tmpdir = tempfile.mkdtemp()

    scenarios = SCENARIOS
    print(f"{'='*60}")
    print(f"  COMPREHENSIVE E2E TEST")
    print(f"  Scenarios: {len(scenarios)}")
    print(f"  Modes: learn, reinforce, mock")
    print(f"  Domains: system_design, algorithms, ai_agent, behavioral")
    print(f"  Personas: {', '.join(PERSONAS.keys())}")
    print(f"  Quick mode: {quick}")
    print(f"{'='*60}")

    all_results = []
    for i, scenario in enumerate(scenarios):
        try:
            result = run_scenario(llm, scenario, syllabus, tmpdir, tracker, quick)
            if result:
                all_results.append(result)
        except Exception as e:
            label = f"{scenario['mode']}/{scenario['domain']}/{scenario['persona']}"
            tracker.add(label, "fatal", "critical", f"Scenario crashed: {e}")
            print(f"    ✗ CRASHED: {e}")

    # ── Final Report ───────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  COMPREHENSIVE E2E REPORT")
    print(f"{'='*60}")

    print(f"\n  Scenarios run: {len(all_results)}/{len(scenarios)}")

    # Summary stats
    total_turns = sum(len(r.get("turns", [])) for r in all_results)
    total_scores = sum(len(r.get("scores", [])) for r in all_results)
    transcripts_saved = sum(1 for r in all_results if r.get("transcript_saved"))
    compressed = sum(1 for r in all_results if r.get("compressed"))
    mastery_nonzero = sum(1 for r in all_results if r.get("mastery", 0) > 0)

    print(f"  Total turns: {total_turns}")
    print(f"  Total scores: {total_scores}")
    print(f"  Transcripts saved: {transcripts_saved}/{len(all_results)}")
    print(f"  Sessions compressed: {compressed}/{len(all_results)}")
    print(f"  Mastery > 0%: {mastery_nonzero}/{len(all_results)}")

    # Issues
    summary = tracker.summary()
    print(f"\n  ISSUES FOUND: {summary['total']}")
    if summary["by_severity"]:
        print(f"  By severity: {json.dumps(summary['by_severity'])}")
    if summary["by_category"]:
        print(f"  By category: {json.dumps(summary['by_category'])}")

    if tracker.issues:
        print(f"\n  ISSUE DETAILS:")
        for issue in tracker.issues:
            print(f"    [{issue['severity'].upper()}] {issue['scenario']}: {issue['category']} — {issue['description']}")

    # Per-scenario results
    print(f"\n  PER-SCENARIO:")
    for r in all_results:
        qs = r.get("quiz_state", {})
        print(f"    {r['label']}: turns={len(r.get('turns',[]))}, "
              f"mastery={r.get('mastery','?')}%, "
              f"scores={len(r.get('scores',[]))}, "
              f"quiz={qs.get('questions',0)}Q "
              f"{'✓' if r.get('transcript_saved') else '✗ transcript'}")

    # Save report
    report_path = os.path.join(tmpdir, "e2e_report.json")
    with open(report_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "scenarios_run": len(all_results),
            "scenarios_total": len(scenarios),
            "issues": tracker.issues,
            "summary": summary,
            "results": [{k: v for k, v in r.items() if k != "turns"} for r in all_results],
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n  Report: {report_path}")

    print(f"\n{'='*60}")
    print(f"  DONE — {summary['total']} issues found")
    print(f"{'='*60}")

    # Don't clean tmpdir so report persists
    print(f"  Temp dir: {tmpdir}")


if __name__ == "__main__":
    main()
