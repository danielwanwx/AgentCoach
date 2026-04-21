from collections import defaultdict
from agentcoach.log import get_logger

logger = get_logger()


def _speak(tts, text: str):
    if tts:
        try:
            tts.speak(text)
        except Exception as e:
            logger.error("tts_failed", error=str(e))


def _bar(pct: int, width: int = 20) -> str:
    """Render a simple ASCII progress bar."""
    filled = int(width * pct / 100)
    return "\u2588" * filled + "\u2591" * (width - filled)


def _show_progress_dashboard(analytics, user_id: str):
    """Display mastery dashboard + per-domain skill growth curves."""
    all_mastery = analytics.get_all_mastery(user_id)
    if not all_mastery:
        print("\n  No practice history yet. Complete a session to start tracking progress.\n")
        return

    # Group by domain
    domains = defaultdict(list)
    for tid, mastery in sorted(all_mastery.items()):
        domain = tid.split(".")[0] if "." in tid else tid
        topic_short = tid.split(".", 1)[1] if "." in tid else tid
        domains[domain].append((topic_short, mastery))

    print("\n  === Mastery Dashboard ===\n")
    for domain, topics in sorted(domains.items()):
        avg = sum(m for _, m in topics) // len(topics)
        print(f"  {domain.replace('_', ' ').title():20s}  {_bar(avg)}  {avg}%")
        for name, mastery in topics:
            print(f"    {name:22s}  {_bar(mastery, 16)}  {mastery}%")
    print()

    # Skill growth curves (per-domain, per-dimension trajectory)
    try:
        from agentcoach.analytics.skill_profile import (
            build_skill_profile, render_growth_curve,
        )
        for domain in sorted(domains.keys()):
            profile = build_skill_profile(analytics, user_id, domain)
            if profile.get("dimensions"):
                print(render_growth_curve(profile))
    except Exception as e:
        logger.error("skill_profile_render_failed", error=str(e))


def _show_pre_session_context(analytics, user_id: str, topic_id: str, topic_name: str):
    """Show relevant mastery context before session starts."""
    summary = analytics.get_topic_summary(user_id, topic_id)
    if not summary or summary["mastery"] == 0:
        return  # first time — nothing to show
    mastery = summary["mastery"]
    print(f"\n  --- Previous Progress: {topic_name} ---")
    print(f"  Current mastery: {_bar(mastery)} {mastery}%")
    if "last_mode" in summary:
        print(f"  Last session: {summary['last_mode']} mode | score delta: {summary['last_score_delta']:+d}")
        if summary.get("last_evidence"):
            print(f"  Last feedback: {summary['last_evidence'][:120]}")
    print()


def _end_session(coach, mem):
    """Generate and save feedback and learning state if there was meaningful conversation."""
    if len(coach.history) > 2:
        print("\nGenerating session wrap-up...")  # UI output
        # Prefer the structured wrap_up (recap + strengths + improvements +
        # 1-10 score) over the older free-form feedback summary.
        try:
            feedback = coach.wrap_up()
        except Exception:
            feedback = coach.get_feedback_summary()
        if feedback:
            print(f"\n{feedback}\n")  # UI output
            mem.save_feedback(feedback)
            logger.info("feedback_saved")
        # Save learning state for cross-session continuity
        qs = coach.quiz_state
        if qs.question_count > 0:
            weak = "; ".join(qs.weak_concepts[-5:]) if qs.weak_concepts else "none"
            learning_entry = (
                f"Topic: {coach.topic_name or 'general'} ({coach.topic_id}) | "
                f"Difficulty reached: {qs.difficulty} | "
                f"Score: {qs.correct_count}/{qs.question_count} | "
                f"Weak areas: {weak}"
            )
            mem.save_learning(learning_entry)
            logger.info("learning_state_saved")


def _score_and_save(coach, analytics, user_id, topic, mode, llm, kb_store=None, syllabus=None, mem=None):
    """Score the session, save results and transcript."""
    if len(coach.history) > 4:
        scores = []
        topic_id = topic["id"] if topic else ""

        # Capture pre-session mastery for delta display
        pre_mastery = analytics.get_mastery(user_id, topic_id) if topic_id else 0

        try:
            from agentcoach.analytics.scorer import Scorer
            from agentcoach.analytics.skill_profile import render_skill_report
            logger.info("session_scoring_start")
            scorer = Scorer(llm, kb_store=kb_store, syllabus=syllabus)
            scores = scorer.score_session(coach.history, mode=mode, topic_id=topic_id)
            if scores:
                print("\n--- Session Scores ---")  # UI output
                for s in scores:
                    analytics.record_score(user_id, s["topic_id"], s["score_delta"], mode, s["evidence"])
                    overall = s.get("overall_score", "?")
                    sign = "+" if s["score_delta"] > 0 else ""
                    print(f"  {s['topic_id']}: {overall}/5 (mastery {sign}{s['score_delta']})")
                    if s.get("evidence"):
                        print(f"  {s['evidence']}")

                # Persist the structured assessment (dimensions + strengths/areas)
                # so the user has a trackable skill profile over time.
                primary = scores[0]
                dims = primary.get("dimensions") or []
                # The scorer currently only returns strengths/areas in its raw dict
                # shape; our condensed evidence field loses them. Re-parse if we
                # still have the raw response stashed on the result, otherwise
                # fall back to whatever was captured in `evidence`.
                strengths = primary.get("strengths") or []
                areas = primary.get("areas_to_improve") or []
                if not strengths and primary.get("evidence"):
                    # Best-effort extraction from "Strengths: a, b. Improve: x, y"
                    ev = primary["evidence"]
                    if "Strengths:" in ev:
                        tail = ev.split("Strengths:", 1)[1]
                        head = tail.split(".", 1)[0]
                        strengths = [s.strip() for s in head.split(",") if s.strip()]
                    if "Improve:" in ev:
                        tail = ev.split("Improve:", 1)[1]
                        head = tail.split(".", 1)[0]
                        areas = [s.strip() for s in head.split(",") if s.strip()]

                resolved_topic = primary.get("topic_id") or topic_id or "general"
                domain = resolved_topic.split(".", 1)[0] if "." in resolved_topic else "general"
                try:
                    analytics.record_assessment(
                        user_id=user_id,
                        topic_id=resolved_topic,
                        domain=domain,
                        mode=mode,
                        overall_score=float(primary.get("overall_score") or 0.0),
                        dimensions=dims,
                        strengths=strengths,
                        areas_to_improve=areas,
                    )
                except Exception as rec_err:
                    logger.error("assessment_persist_failed", error=str(rec_err))

                # Candidate-facing skill report (dimension bars + focus areas)
                post_mastery = analytics.get_mastery(user_id, topic_id) if topic_id else None
                try:
                    report_payload = {
                        "topic_id": resolved_topic,
                        "mode": mode,
                        "overall_score": float(primary.get("overall_score") or 0.0),
                        "dimensions": dims,
                        "strengths": strengths,
                        "areas_to_improve": areas,
                    }
                    print(render_skill_report(
                        report_payload,
                        mastery_before=pre_mastery,
                        mastery_after=post_mastery,
                    ))
                except Exception as ren_err:
                    logger.error("skill_report_render_failed", error=str(ren_err))

                # Suggest next step based on mastery
                if topic_id and post_mastery is not None:
                    if post_mastery < 40:
                        print("  Next: continue in learn mode")
                    elif post_mastery < 70:
                        print("  Next: try reinforce mode to solidify")
                    else:
                        print("  Next: ready for mock interview!")
                print()
            else:
                print("\n  [Scorer returned no results — check LLM response format]\n")
        except Exception as e:
            logger.error("scoring_failed", error=str(e))
        # Save complete session transcript for review
        if mem:
            try:
                mem.save_transcript(
                    user_id=user_id,
                    topic_id=topic["id"] if topic else "",
                    topic_name=topic["name"] if topic else "general",
                    mode=mode,
                    history=coach.history,
                    scores=scores,
                )
                logger.info("transcript_saved")
            except Exception as e:
                logger.error("transcript_save_failed", error=str(e))


def _run_session(coach, mem, tts, analytics, user_id, topic, mode, llm, kb_store=None, syllabus=None):
    """Run an interactive session until user quits."""
    # Show pre-session context if user has history on this topic
    if topic:
        _show_pre_session_context(analytics, user_id, topic["id"], topic["name"])

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            _end_session(coach, mem)
            _score_and_save(coach, analytics, user_id, topic, mode, llm, kb_store=kb_store, syllabus=syllabus, mem=mem)
            print("\nSession ended.")  # UI output
            return

        if not user_input:
            continue
        if user_input.lower() in ("quit", "done", "exit"):
            _end_session(coach, mem)
            _score_and_save(coach, analytics, user_id, topic, mode, llm, kb_store=kb_store, syllabus=syllabus, mem=mem)
            print("Session ended.")  # UI output
            return
        if user_input.lower() == "memory":
            ctx = mem.get_context()
            print(f"\n{ctx}\n" if ctx else "No memory stored yet.\n")  # UI output
            continue
        if user_input.lower() == "progress":
            _show_progress_dashboard(analytics, user_id)
            continue

        response = coach.respond(user_input)
        print(f"\nCoach: {response}\n")  # UI output
        _speak(tts, response)
