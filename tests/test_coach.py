from unittest.mock import MagicMock
from agentcoach.coach import Coach
from agentcoach.llm.base import Message

def test_coach_start_sends_system_prompt():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Hi! What role are you targeting?"

    coach = Coach(llm=mock_llm, mode="behavioral")
    response = coach.start()

    assert response == "Hi! What role are you targeting?"
    call_args = mock_llm.generate.call_args[0][0]
    assert call_args[0].role == "system"
    assert "behavioral" in call_args[0].content.lower()

def test_coach_respond_maintains_history():
    mock_llm = MagicMock()
    mock_llm.generate.side_effect = [
        "Hi! What role?",
        "Great. Tell me about a time you led a project.",
    ]

    coach = Coach(llm=mock_llm, mode="behavioral")
    coach.start()
    response = coach.respond("I'm targeting AI Engineer roles.")

    assert response == "Great. Tell me about a time you led a project."
    call_args = mock_llm.generate.call_args[0][0]
    assert len(call_args) == 4
