from agentcoach.prompt.templates import build_system_prompt


def test_build_prompt_with_context():
    context = "### User Profile\n- SWE, 5 years Python"
    prompt = build_system_prompt("behavioral", context)
    assert "behavioral" in prompt.lower()
    assert "SWE" in prompt
    assert "Python" in prompt


def test_build_prompt_without_context():
    prompt = build_system_prompt("behavioral", "")
    assert "behavioral" in prompt.lower()
    assert "User Profile" not in prompt
