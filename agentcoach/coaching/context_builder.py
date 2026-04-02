from agentcoach.llm.base import Message
from agentcoach.prompt.templates import build_system_prompt, QUIZ_STATE_SECTION
from agentcoach.coaching.quiz_state import DIFFICULTY_LABELS


def update_kb_context(kb_store, query, mode, memory_context, kb_teaching_context, history):
    """Search KB and update system prompt with relevant knowledge."""
    try:
        results = kb_store.search(query, limit=3)
        if results:
            kb_text = "\n".join(
                f"- [{r['section']}] {r['content'][:500]}"
                for r in results
            )
            updated_prompt = build_system_prompt(
                mode, memory_context, kb_context=kb_text,
                kb_teaching_content=kb_teaching_context,
            )
            history[0] = Message(role="system", content=updated_prompt)
    except Exception:
        pass  # KB search failure should not break the interview


def refresh_system_prompt(quiz_state, mode, memory_context, kb_teaching_context, history):
    """Rebuild system prompt with current quiz state."""
    qs = quiz_state
    weak_line = ""
    if qs.weak_concepts:
        weak_line = "Weak areas: " + "; ".join(qs.weak_concepts[-3:])
    quiz_ctx = QUIZ_STATE_SECTION.format(
        question_num=qs.question_count,
        correct=qs.correct_count,
        incorrect=qs.incorrect_count,
        difficulty_label=DIFFICULTY_LABELS.get(qs.difficulty, "Concept recall"),
        weak_concepts_line=weak_line,
    )
    updated = build_system_prompt(
        mode, memory_context,
        kb_teaching_content=kb_teaching_context,
        quiz_state_context=quiz_ctx,
    )
    history[0] = Message(role="system", content=updated)


def inject_strategy(mode, quiz_state, user_input, history_len):
    """Select teaching strategy. Returns strategy prompt string or None."""
    try:
        from agentcoach.coaching.strategies import (
            select_strategy, get_strategy_prompt, detect_confusion,
        )
        qs = quiz_state
        confused = detect_confusion(user_input)
        strategy = select_strategy(
            mode=mode,
            topic_mastery=0.0,  # TODO: get from analytics
            consecutive_wrong=qs.incorrect_count - qs.correct_count if qs.incorrect_count > qs.correct_count else 0,
            consecutive_right=qs._consecutive_correct,
            turn_number=history_len // 2,
            user_said_confused=confused,
        )
        return get_strategy_prompt(strategy)
    except Exception:
        return None
