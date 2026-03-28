from agentcoach.prompt.templates import get_coach_system_prompt


def test_behavioral_system_prompt():
    prompt = get_coach_system_prompt("behavioral")
    assert "interview" in prompt.lower()
    assert "behavioral" in prompt.lower()
    assert len(prompt) > 100


def test_unknown_mode_raises():
    import pytest
    with pytest.raises(ValueError):
        get_coach_system_prompt("unknown_mode")
