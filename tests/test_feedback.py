from unittest.mock import MagicMock
from agentcoach.coach import Coach


def test_get_feedback_summary():
    mock_llm = MagicMock()
    mock_llm.generate.side_effect = [
        "Hi! What role are you targeting?",
        "Great question response.",
        "Summary: Strength - good technical depth. Weakness - needs more metrics. Score: 7/10."
    ]

    coach = Coach(llm=mock_llm, mode="behavioral")
    coach.start()
    coach.respond("I'm targeting AI Engineer roles at top companies.")

    feedback = coach.get_feedback_summary()
    assert "Strength" in feedback or "Weakness" in feedback or "Score" in feedback or "Summary" in feedback


def test_get_feedback_summary_short_history():
    """No feedback if conversation is too short."""
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Hi! What role are you targeting?"

    coach = Coach(llm=mock_llm, mode="behavioral")
    # Only system prompt in history, no start() call
    feedback = coach.get_feedback_summary()
    assert feedback == ""


def test_get_feedback_summary_after_start_only():
    """No feedback if only the opening message exists (system + assistant = 2 entries)."""
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Hi! What role are you targeting?"

    coach = Coach(llm=mock_llm, mode="behavioral")
    coach.start()
    feedback = coach.get_feedback_summary()
    assert feedback == ""
