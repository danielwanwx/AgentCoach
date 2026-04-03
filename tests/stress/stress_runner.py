"""Stress test runner -- runs a full coaching session end-to-end.

Initializes all real AgentCoach components, simulates a candidate via LLM,
records transcripts, scores the session, and generates a quality report.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime

from agentcoach.llm.base import Message
from agentcoach.llm.router import LLMRouter
from agentcoach.coaching.coach import Coach, strip_markdown
from agentcoach.analytics.scorer import Scorer
from agentcoach.analytics.store import AnalyticsStore
from agentcoach.memory.store import CoachMemory
from agentcoach.kb.store import KnowledgeStore
from agentcoach.syllabus.loader import SyllabusLoader

from tests.stress.scenarios import Scenario


def _say(text: str, voice: str = "Daniel", rate: int = 155):
    """Speak text using macOS say command."""
    clean = strip_markdown(text)
    if not clean:
        return
    # Truncate very long responses for TTS
    if len(clean) > 800:
        clean = clean[:800] + "..."
    subprocess.run(["say", "-v", voice, "-r", str(rate), "--", clean])


def _generate_candidate_reply(llm, scenario: Scenario, coach_message: str,
                              turn_number: int, conversation_so_far: list) -> str:
    """Use the LLM to generate a realistic candidate reply."""
    # Keep persona short to avoid MiniMax 400 errors with long system prompts
    persona_short = scenario.persona_prompt[:500] if scenario.persona_prompt else ""
    prompt = (
        f"You are Daniel, a 6-year Senior Data Engineer preparing for Meta E5 interview.\n"
        f"{persona_short}\n\n"
        f"Mode: {scenario.mode}, Topic: {scenario.topic_id}, Turn: {turn_number}\n"
        f"Keep answers 2-5 sentences. Respond naturally.\n\n"
        f"Coach said:\n{coach_message[:800]}\n\nRespond as Daniel:"
    )
    messages = [Message(role="user", content=prompt)]
    try:
        return llm.generate(messages)
    except Exception as e:
        return f"Hmm, let me think about that... can you explain a bit more?"


def _evaluate_session_quality(llm, scenario: Scenario, history: list,
                              scores: list) -> dict:
    """Use LLM to evaluate the overall quality of the coaching session."""
    # Build transcript summary
    transcript_lines = []
    for msg in history:
        if msg.role == "system":
            continue
        speaker = "Coach" if msg.role == "assistant" else "Candidate"
        transcript_lines.append(f"{speaker}: {msg.content[:300]}")
    transcript_text = "\n".join(transcript_lines[-20:])  # last 20 exchanges

    score_text = json.dumps(scores, indent=2) if scores else "No scores available"

    eval_prompt = f"""Evaluate this AgentCoach stress test session.

Scenario: {scenario.name}
Mode: {scenario.mode}
Topic: {scenario.topic_id}
Company: {scenario.company}

## Session Transcript (last exchanges)
{transcript_text}

## Scorer Output
{score_text}

Rate the session on these dimensions (1-5 each):
1. **Coach Quality**: Did the coach ask good questions, give useful feedback, stay on topic?
2. **Candidate Realism**: Did the simulated candidate behave realistically?
3. **Topic Coverage**: Was the topic adequately explored for the mode ({scenario.mode})?
4. **Progression**: Did the session build logically from simple to complex?
5. **Actionable Feedback**: Did the coach provide specific, actionable improvement suggestions?

Return ONLY a JSON object:
{{
  "coach_quality": <int 1-5>,
  "candidate_realism": <int 1-5>,
  "topic_coverage": <int 1-5>,
  "progression": <int 1-5>,
  "actionable_feedback": <int 1-5>,
  "overall": <float 1.0-5.0>,
  "notes": "<one sentence summary>"
}}"""
    try:
        import re
        response = llm.generate([Message(role="user", content=eval_prompt)])
        match = re.search(r'\{[\s\S]*\}', response)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"  [eval error] {e}")
    return {"overall": 0, "notes": "Evaluation failed"}


def run_scenario(scenario: Scenario, voice: bool = True,
                 min_turns_override: int = None) -> dict:
    """Run a single stress test scenario end-to-end.

    Returns a result dict with transcript, scores, and quality evaluation.
    """
    min_turns = min_turns_override or scenario.min_turns
    print(f"\n{'='*60}")
    print(f"STRESS TEST: {scenario.name}")
    print(f"  Mode: {scenario.mode} | Topic: {scenario.topic_id} | Turns: {min_turns}")
    print(f"{'='*60}\n")

    # --- Initialize components ---
    router = LLMRouter.from_env()
    coach_llm = router.get("coaching")
    # Use coaching LLM for scoring too — avoids API key scope issues
    # and ensures the scorer actually works with the available provider
    scorer_llm = router.get("coaching")

    # Use temp directories for stress test databases (avoid polluting real data)
    tmp_dir = tempfile.mkdtemp(prefix="agentcoach_stress_")
    memory = CoachMemory(db_path=os.path.join(tmp_dir, "memory.db"))
    analytics = AnalyticsStore(db_path=os.path.join(tmp_dir, "analytics.db"))
    kb_store = KnowledgeStore(
        db_path=os.path.join(tmp_dir, "knowledge.db"),
        use_vectors=False,
    )
    syllabus = SyllabusLoader()

    # Resolve topic name from syllabus
    topic_info = syllabus.get_topic(scenario.topic_id)
    topic_name = topic_info["name"] if topic_info else scenario.topic_id

    # Build memory context for the candidate persona
    memory_context = (
        f"### User Profile\n"
        f"- Name: Daniel\n"
        f"- Current role: Sr Data Engineer at Disney (6yr exp)\n"
        f"- Targeting: {scenario.company} E5\n"
        f"- Weak areas: system design breadth, behavioral storytelling"
    )

    # Get KB teaching context for learn/reinforce modes
    kb_teaching_context = ""
    if scenario.mode in ("learn", "reinforce"):
        # Try to get relevant KB content
        try:
            results = kb_store.search(scenario.topic_id, limit=3,
                                       category=scenario.domain)
            if results:
                kb_teaching_context = "\n".join(
                    f"- {r['content'][:500]}" for r in results
                )
        except Exception:
            pass

    # --- Create Coach ---
    coach = Coach(
        llm=coach_llm,
        mode=scenario.mode,
        memory_context=memory_context,
        kb_store=kb_store,
        topic_id=scenario.topic_id,
        topic_name=topic_name,
        kb_teaching_context=kb_teaching_context,
    )

    # --- Start session ---
    print(f"[Coach] Starting session...")
    start_time = time.time()
    opening = coach.start()
    print(f"[Coach] {opening[:200]}...")
    if voice:
        _say(opening, voice="Daniel", rate=155)

    # --- Conversation loop ---
    turn_count = 0
    while turn_count < min_turns:
        turn_count += 1
        print(f"\n--- Turn {turn_count}/{min_turns} ---")

        # Generate candidate reply
        candidate_reply = _generate_candidate_reply(
            coach_llm, scenario, opening if turn_count == 1 else coach_response,
            turn_count, coach.history,
        )
        print(f"[Candidate] {candidate_reply[:200]}...")
        if voice:
            _say(candidate_reply, voice="Samantha", rate=175)

        # Get coach response
        coach_response = coach.respond(candidate_reply)
        print(f"[Coach] {coach_response[:200]}...")
        if voice:
            _say(coach_response, voice="Daniel", rate=155)

    elapsed = time.time() - start_time

    # --- Score the session ---
    print(f"\n[Scoring] Running Scorer on {len(coach.history)} messages...")
    scorer = Scorer(llm=scorer_llm, kb_store=kb_store, syllabus=syllabus)
    scores = scorer.score_session(
        history=coach.history,
        mode=scenario.mode,
        topic_id=scenario.topic_id,
    )
    print(f"[Scoring] Result: {json.dumps(scores, indent=2)}")

    # --- Save transcript and learning ---
    user_id = "stress_test_daniel"
    memory.save_transcript(
        user_id=user_id,
        topic_id=scenario.topic_id,
        topic_name=topic_name,
        mode=scenario.mode,
        history=coach.history,
        scores=scores,
    )
    # Save a learning memory entry summarizing the session
    if scores:
        score_summary = scores[0] if scores else {}
        learning_entry = (
            f"Stress test session: {scenario.name} | "
            f"Score delta: {score_summary.get('score_delta', 'N/A')} | "
            f"Overall: {score_summary.get('overall_score', 'N/A')}"
        )
        memory.save_learning(learning_entry)

    # Record in analytics
    for s in scores:
        analytics.record_score(
            user_id=user_id,
            topic_id=s.get("topic_id", scenario.topic_id),
            score_delta=s.get("score_delta", 0),
            mode=scenario.mode,
            evidence=s.get("evidence", ""),
        )

    # --- Evaluate quality ---
    print(f"\n[Quality] Evaluating session quality...")
    quality = _evaluate_session_quality(coach_llm, scenario, coach.history, scores)
    print(f"[Quality] Overall: {quality.get('overall', 'N/A')}/5 -- {quality.get('notes', '')}")

    # --- Build result ---
    result = {
        "scenario": scenario.name,
        "topic_id": scenario.topic_id,
        "mode": scenario.mode,
        "company": scenario.company,
        "turns": turn_count,
        "elapsed_seconds": round(elapsed, 1),
        "history_length": len(coach.history),
        "scores": scores,
        "quality": quality,
        "tmp_dir": tmp_dir,
    }
    return result


def generate_report(results: list, output_path: str = ""):
    """Generate a markdown report from stress test results."""
    if not output_path:
        output_path = os.path.join(
            os.path.dirname(__file__),
            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        )

    lines = [
        "# AgentCoach Stress Test Report",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Scenarios Run**: {len(results)}",
        "",
    ]

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| # | Scenario | Mode | Topic | Turns | Time(s) | Score | Quality |")
    lines.append("|---|----------|------|-------|-------|---------|-------|---------|")
    for i, r in enumerate(results, 1):
        score_val = ""
        if r.get("scores"):
            s = r["scores"][0]
            score_val = f"{s.get('overall_score', s.get('score_delta', '?'))}"
        quality_val = r.get("quality", {}).get("overall", "?")
        lines.append(
            f"| {i} | {r['scenario']} | {r['mode']} | {r['topic_id']} | "
            f"{r['turns']} | {r['elapsed_seconds']} | {score_val} | {quality_val} |"
        )

    lines.append("")

    # Detailed results
    lines.append("## Detailed Results")
    lines.append("")
    for i, r in enumerate(results, 1):
        lines.append(f"### {i}. {r['scenario']}")
        lines.append(f"- **Mode**: {r['mode']}")
        lines.append(f"- **Topic**: {r['topic_id']}")
        lines.append(f"- **Company**: {r['company']}")
        lines.append(f"- **Turns**: {r['turns']} | **Time**: {r['elapsed_seconds']}s")
        lines.append(f"- **History messages**: {r['history_length']}")
        if r.get("scores"):
            s = r["scores"][0]
            lines.append(f"- **Score delta**: {s.get('score_delta', 'N/A')}")
            lines.append(f"- **Overall score**: {s.get('overall_score', 'N/A')}")
            lines.append(f"- **Evidence**: {s.get('evidence', 'N/A')}")
        q = r.get("quality", {})
        if q:
            lines.append(f"- **Quality overall**: {q.get('overall', 'N/A')}/5")
            for dim in ["coach_quality", "candidate_realism", "topic_coverage",
                        "progression", "actionable_feedback"]:
                lines.append(f"  - {dim}: {q.get(dim, '?')}/5")
            lines.append(f"- **Notes**: {q.get('notes', '')}")
        lines.append("")

    report_text = "\n".join(lines)

    with open(output_path, "w") as f:
        f.write(report_text)
    print(f"\nReport written to: {output_path}")
    return output_path
