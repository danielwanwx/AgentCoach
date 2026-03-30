from agentcoach.prompt.templates import get_coach_system_prompt

def test_learn_prompt():
    prompt = get_coach_system_prompt("learn")
    assert "quiz" in prompt.lower() or "question" in prompt.lower()

def test_reinforce_prompt():
    prompt = get_coach_system_prompt("reinforce")
    assert "follow" in prompt.lower() or "deeper" in prompt.lower()

def test_mock_system_design_prompt():
    prompt = get_coach_system_prompt("mock_system_design")
    assert "design" in prompt.lower()

def test_mock_algorithms_prompt():
    prompt = get_coach_system_prompt("mock_algorithms")
    assert "algorithm" in prompt.lower() or "coding" in prompt.lower()

def test_mock_ai_agent_prompt():
    prompt = get_coach_system_prompt("mock_ai_agent")
    assert "agent" in prompt.lower() or "llm" in prompt.lower()

def test_mock_behavioral_prompt():
    prompt = get_coach_system_prompt("mock_behavioral")
    assert "behavioral" in prompt.lower()
