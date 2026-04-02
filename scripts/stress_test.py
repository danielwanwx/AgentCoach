#!/usr/bin/env python3
"""Stress test: evaluate Coach quality across adversarial scenarios.

Tests Coach's ability to:
1. Adapt to different user levels (beginner → expert)
2. Handle unexpected/off-topic questions gracefully
3. Demonstrate KB mastery (cite sources, not hallucinate)
4. Correct misconceptions without being condescending
5. Push users to think deeper, not just give answers
6. Maintain conversation coherence over 10+ turns
7. Transition smoothly between teaching → quizzing → feedback

Each scenario has an evaluator that scores Coach quality on multiple dimensions.
"""
from __future__ import annotations
import os, sys, re, json, tempfile, time
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
import subprocess


# ── Adversarial Personas ───────────────────────────────────────

STRESS_PERSONAS = {
    "confused_beginner": {
        "system": "You are completely lost. Every response should show genuine confusion. "
                  "Ask 'what does that mean?' frequently. Misunderstand explanations. "
                  "Mix up terminology constantly. Say things like 'wait I'm so confused'. 2-3 sentences.",
        "challenge": "Can Coach patiently re-explain without getting repetitive?",
    },
    "overconfident_wrong": {
        "system": "You are confident but WRONG about almost everything. State incorrect facts "
                  "as if they're obvious. Push back when corrected: 'No, I'm pretty sure that's right'. "
                  "Only reluctantly accept corrections with strong evidence. 2-4 sentences.",
        "challenge": "Can Coach firmly but respectfully correct without caving?",
    },
    "topic_jumper": {
        "system": "You keep jumping between topics mid-conversation. Start talking about caching, "
                  "then suddenly ask about databases, then ask about an unrelated algorithm. "
                  "You have ADHD energy. 2-3 sentences.",
        "challenge": "Can Coach redirect back to topic without being dismissive?",
    },
    "silent_minimal": {
        "system": "You give the shortest possible answers. One word or one short sentence max. "
                  "'Yes.' 'No.' 'I think so.' 'Cache.' Never elaborate unless directly asked. "
                  "You're shy or disengaged.",
        "challenge": "Can Coach draw out more detailed responses?",
    },
    "expert_tester": {
        "system": "You already know the topic well. Ask tricky edge-case questions to test the "
                  "Coach's depth. Point out if the Coach oversimplifies. Challenge with 'but what "
                  "about...' scenarios. You want to learn nuances, not basics. 3-5 sentences.",
        "challenge": "Can Coach handle expert-level questions without bluffing?",
    },
    "anxious_interviewer": {
        "system": "You're extremely anxious about your upcoming interview. Keep saying things like "
                  "'I'm going to fail' and 'this is too hard'. Ask for reassurance. Sometimes "
                  "refuse to try: 'I don't know, just tell me the answer'. 2-3 sentences.",
        "challenge": "Can Coach provide emotional support while still pushing learning?",
    },
}

# ── Scenarios ──────────────────────────────────────────────────

STRESS_SCENARIOS = [
    # Learn mode stress tests
    {"mode": "learn", "domain": "system_design", "topic_id": "system_design.caching",
     "topic_name": "Caching", "persona": "confused_beginner", "turns": 12,
     "eval_focus": "patience, re-explanation quality, analogy usage"},
    {"mode": "learn", "domain": "system_design", "topic_id": "system_design.sharding",
     "topic_name": "Sharding", "persona": "overconfident_wrong", "turns": 12,
     "eval_focus": "correction firmness, evidence citation, diplomacy"},
    {"mode": "learn", "domain": "ai_agent", "topic_id": "ai_agent.rag",
     "topic_name": "RAG", "persona": "topic_jumper", "turns": 10,
     "eval_focus": "topic management, redirection skill, flexibility"},
    {"mode": "learn", "domain": "algorithms", "topic_id": "algorithms.binary_search",
     "topic_name": "Binary Search", "persona": "silent_minimal", "turns": 10,
     "eval_focus": "engagement techniques, question quality, drawing out answers"},

    # Reinforce stress tests
    {"mode": "reinforce", "domain": "system_design", "topic_id": "system_design.caching",
     "topic_name": "Caching Deep Dive", "persona": "expert_tester", "turns": 12,
     "eval_focus": "depth of knowledge, handling edge cases, honesty about limits"},
    {"mode": "reinforce", "domain": "ai_agent", "topic_id": "ai_agent.transformer",
     "topic_name": "Transformer Architecture", "persona": "anxious_interviewer", "turns": 10,
     "eval_focus": "emotional support, confidence building, gentle pushing"},

    # Mock interview stress tests
    {"mode": "mock", "domain": "system_design", "topic_id": "system_design.url_shortener",
     "topic_name": "Design URL Shortener", "persona": "overconfident_wrong", "turns": 12,
     "eval_focus": "interview realism, pushback quality, fair scoring"},
    {"mode": "mock", "domain": "behavioral", "topic_id": "behavioral.conflict",
     "topic_name": "Conflict Resolution", "persona": "anxious_interviewer", "turns": 10,
     "eval_focus": "empathy, structure, helping candidate find stories"},
]

# ── Turn behaviors ─────────────────────────────────────────────

def get_behavior(mode, turn, total):
    """Dynamic behavior based on mode and conversation phase."""
    phase = turn / total  # 0.0 → 1.0

    if mode == "learn":
        if phase < 0.2: return "React to the opening. Stay in character."
        if phase < 0.5: return "Engage with what coach is teaching. Stay in character."
        if phase < 0.7: return "Coach should be quizzing now. Answer in character."
        return "Reflect on the session. Stay in character."
    elif mode == "reinforce":
        if phase < 0.3: return "Answer the practice question. Stay in character."
        if phase < 0.7: return "Engage with deeper questions. Stay in character."
        return "Summarize what you've practiced. Stay in character."
    else:  # mock
        if phase < 0.15: return "Ask clarifying questions about the problem."
        if phase < 0.3: return "Propose high-level design."
        if phase < 0.6: return "Answer follow-up questions. Stay in character."
        if phase < 0.8: return "Handle pushback. Stay in character."
        return "Wrap up the interview. Stay in character."


# ── Evaluator ──────────────────────────────────────────────────

EVAL_PROMPT = """You are evaluating an AI tutoring Coach's performance. Score each dimension 1-5.

Session mode: {mode}
Persona type: {persona} — {challenge}
Evaluation focus: {eval_focus}

Score these dimensions (1=terrible, 3=adequate, 5=excellent):

1. ADAPTABILITY: Did the Coach adapt to this specific user's level and style?
2. KB_MASTERY: Did the Coach demonstrate deep knowledge, cite sources, avoid hallucination?
3. PEDAGOGY: Did the Coach teach effectively (analogies, scaffolding, checking understanding)?
4. CORRECTION: When the user was wrong, did the Coach correct firmly but respectfully?
5. ENGAGEMENT: Did the Coach keep the user engaged and draw out deeper thinking?
6. COHERENCE: Did the conversation flow naturally over multiple turns?
7. EMOTIONAL_IQ: Did the Coach handle the user's emotional state appropriately?

Return ONLY a JSON object:
{{"adaptability": N, "kb_mastery": N, "pedagogy": N, "correction": N, "engagement": N, "coherence": N, "emotional_iq": N, "overall": N, "issues": ["issue1", "issue2"], "strengths": ["strength1"]}}

Conversation transcript:
{transcript}"""


def evaluate_session(llm, mode, persona_key, challenge, eval_focus, history):
    """Use LLM to evaluate Coach quality."""
    transcript = ""
    for msg in history:
        if msg.role == "system":
            continue
        role = "Coach" if msg.role == "assistant" else "User"
        transcript += f"\n{role}: {msg.content[:300]}\n"

    prompt = EVAL_PROMPT.format(
        mode=mode, persona=persona_key, challenge=challenge,
        eval_focus=eval_focus, transcript=transcript[:4000],
    )

    try:
        response = llm.generate([Message(role="user", content=prompt)])
        match = re.search(r'\{[\s\S]*\}', response)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return None


# ── Run scenario ───────────────────────────────────────────────

def run_stress(llm, scenario, syllabus, tmpdir):
    mode = scenario["mode"]
    topic_id = scenario["topic_id"]
    topic_name = scenario["topic_name"]
    persona_key = scenario["persona"]
    persona = STRESS_PERSONAS[persona_key]
    turns = scenario["turns"]
    eval_focus = scenario["eval_focus"]

    label = f"{mode}/{scenario['domain']}/{persona_key}"
    print(f"\n  🔥 {label} ({topic_name}, {turns}t)")
    print(f"     Challenge: {persona['challenge']}")

    analytics = AnalyticsStore(db_path=os.path.join(tmpdir, f"{label.replace('/','_')}.db"))
    mem = CoachMemory(db_path=os.path.join(tmpdir, f"{label.replace('/','_')}_mem.db"))
    kb = KnowledgeStore(db_path=os.path.join(tmpdir, f"{label.replace('/','_')}_kb.db"), use_vectors=False)

    # Load real KB from qmd
    for doc_id in ["#ccdec4", "#f1b14c"]:
        result = subprocess.run(["qmd", "get", doc_id, "--full"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            sections = re.split(r'\n(?=#{1,3} )', result.stdout.strip())
            for sec in sections:
                lines = sec.strip().split('\n')
                title = lines[0].lstrip('#').strip() if lines else ""
                body = re.sub(r'<[^>]+>', '', '\n'.join(lines[1:]).strip())
                if len(body) > 80:
                    kb.add_chunk(content=body[:800], source="sd-books",
                                 section=title, category=scenario["domain"])

    # Pre-record prereqs for reinforce/mock
    if mode in ("reinforce", "mock"):
        topic = syllabus.get_topic(topic_id)
        if topic:
            for prereq in topic.get("prerequisites", []):
                analytics.record_score("stress", prereq, 50, "mock")
            analytics.record_score("stress", topic_id, 30, "learn")

    prompt_mode = f"mock_{scenario['domain']}" if mode == "mock" else mode

    kb_results = kb.search(topic_name, limit=5)
    kb_teaching = "\n\n".join(r["content"][:500] for r in kb_results) if mode == "learn" else ""

    hint = ("\nKeep responses to 4 sentences max. Be conversational. "
            "NO code blocks, NO tables. Teach one concept at a time.")

    coach = Coach(
        llm=llm, mode=prompt_mode, kb_store=kb,
        topic_id=topic_id, topic_name=topic_name,
        kb_teaching_context=kb_teaching,
        memory_context=mem.get_context() + hint,
    )

    # Run conversation
    opening = coach.start()
    print(f"     Coach: {opening[:100]}...")
    last_coach = opening

    for turn in range(turns):
        behavior = get_behavior(mode, turn, turns)
        msgs = [
            Message(role="system", content=persona["system"]),
            Message(role="user", content=(
                f"Topic: {topic_name}\nCoach said:\n{last_coach[:400]}\n\n"
                f"Behavior: {behavior}\nReply (stay in character):"
            )),
        ]
        try:
            student = llm.generate(msgs)
        except Exception:
            student = "Can you repeat that?"

        print(f"     {persona_key} ({turn+1}/{turns}): {student[:80]}...")

        response = coach.respond(student)
        print(f"     Coach: {response[:80]}...")
        last_coach = response

    # Evaluate
    print(f"     Evaluating...")
    evaluation = evaluate_session(
        llm, mode, persona_key, persona["challenge"],
        eval_focus, coach.history,
    )

    # Score
    scorer = Scorer(llm, kb_store=kb, syllabus=syllabus)
    scores = scorer.score_session(coach.history, mode=mode, topic_id=topic_id)
    for s in scores:
        analytics.record_score("stress", s["topic_id"], s["score_delta"], mode, s["evidence"])
    mastery = analytics.get_mastery("stress", topic_id)

    # Save transcript
    mem.save_transcript("stress", topic_id, topic_name, mode, coach.history, scores)

    result = {
        "label": label,
        "topic": topic_name,
        "persona": persona_key,
        "turns": turns,
        "mastery": mastery,
        "evaluation": evaluation,
        "scores": scores,
        "history_len": len(coach.history),
    }

    if evaluation:
        avg = sum(v for k, v in evaluation.items() if isinstance(v, (int, float)) and k != "overall") / 7
        result["avg_score"] = round(avg, 1)
        print(f"     ✓ mastery={mastery}% avg_eval={avg:.1f}/5")
        if evaluation.get("issues"):
            for issue in evaluation["issues"][:3]:
                print(f"       ⚠ {issue}")
    else:
        print(f"     ✓ mastery={mastery}% (eval failed)")

    return result


# ── Main ───────────────────────────────────────────────────────

def main():
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "minimax")
    model_name = os.getenv("LLM_MODEL", "")
    if not api_key:
        print("Error: Set LLM_API_KEY"); sys.exit(1)

    llm = OpenAICompatAdapter(api_key=api_key, provider=provider, model=model_name)
    syllabus = SyllabusLoader()
    tmpdir = tempfile.mkdtemp()

    print("=" * 60)
    print("  STRESS TEST: Coach Quality Evaluation")
    print(f"  Scenarios: {len(STRESS_SCENARIOS)}")
    print(f"  Personas: {', '.join(STRESS_PERSONAS.keys())}")
    print("=" * 60)

    all_results = []
    for scenario in STRESS_SCENARIOS:
        try:
            result = run_stress(llm, scenario, syllabus, tmpdir)
            all_results.append(result)
        except Exception as e:
            print(f"     ✗ CRASHED: {e}")

    # ── Report ─────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  STRESS TEST REPORT")
    print(f"{'='*60}")

    all_issues = []
    all_strengths = []
    dim_scores = {d: [] for d in ["adaptability", "kb_mastery", "pedagogy", "correction",
                                   "engagement", "coherence", "emotional_iq"]}

    for r in all_results:
        ev = r.get("evaluation", {})
        if ev:
            for dim in dim_scores:
                if dim in ev and isinstance(ev[dim], (int, float)):
                    dim_scores[dim].append(ev[dim])
            all_issues.extend(ev.get("issues", []))
            all_strengths.extend(ev.get("strengths", []))

    print(f"\n  DIMENSION AVERAGES (1-5):")
    for dim, scores in dim_scores.items():
        avg = sum(scores) / len(scores) if scores else 0
        bar = "█" * int(avg) + "░" * (5 - int(avg))
        status = "✓" if avg >= 3.5 else "⚠" if avg >= 2.5 else "✗"
        print(f"    {status} {dim:15s}: {avg:.1f} {bar}")

    overall_avg = sum(sum(s)/len(s) for s in dim_scores.values() if s) / len(dim_scores)
    print(f"\n    OVERALL: {overall_avg:.1f}/5.0")

    if all_issues:
        # Deduplicate similar issues
        unique_issues = list(set(all_issues))
        print(f"\n  ISSUES ({len(unique_issues)} unique):")
        for issue in unique_issues[:15]:
            print(f"    ⚠ {issue}")

    if all_strengths:
        unique_strengths = list(set(all_strengths))
        print(f"\n  STRENGTHS ({len(unique_strengths)} unique):")
        for s in unique_strengths[:10]:
            print(f"    ✓ {s}")

    print(f"\n  PER-SCENARIO:")
    for r in all_results:
        ev = r.get("evaluation", {})
        avg = r.get("avg_score", 0)
        print(f"    {r['label']:40s} avg={avg}/5 mastery={r['mastery']}%")

    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "scenarios": len(all_results),
        "dimension_averages": {d: round(sum(s)/len(s), 1) if s else 0 for d, s in dim_scores.items()},
        "overall": round(overall_avg, 1),
        "issues": list(set(all_issues)),
        "strengths": list(set(all_strengths)),
        "results": all_results,
    }
    report_path = os.path.join(tmpdir, "stress_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n  Report: {report_path}")
    print(f"\n{'='*60}")
    print(f"  DONE — overall {overall_avg:.1f}/5.0")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
