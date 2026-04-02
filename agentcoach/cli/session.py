from agentcoach.log import get_logger

logger = get_logger()


def _speak(tts, text: str):
    if tts:
        try:
            tts.speak(text)
        except Exception as e:
            logger.error("tts_failed", error=str(e))


def _end_session(coach, mem):
    """Generate and save feedback and learning state if there was meaningful conversation."""
    if len(coach.history) > 2:
        print("\nGenerating session feedback...")  # UI output
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
        try:
            from agentcoach.analytics.scorer import Scorer
            logger.info("session_scoring_start")
            scorer = Scorer(llm, kb_store=kb_store, syllabus=syllabus)
            topic_id = topic["id"] if topic else ""
            scores = scorer.score_session(coach.history, mode=mode, topic_id=topic_id)
            if scores:
                print("\n--- Session Scores ---")  # UI output
                for s in scores:
                    analytics.record_score(user_id, s["topic_id"], s["score_delta"], mode, s["evidence"])
                    sign = "+" if s["score_delta"] > 0 else ""
                    print(f"  {s['topic_id']}: {sign}{s['score_delta']} -- {s['evidence']}")  # UI output
                print()  # UI output
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

        response = coach.respond(user_input)
        print(f"\nCoach: {response}\n")  # UI output
        _speak(tts, response)
