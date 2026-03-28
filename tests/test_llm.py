from agentcoach.llm.base import LLMAdapter, Message


def test_message_creation():
    msg = Message(role="user", content="hello")
    assert msg.role == "user"
    assert msg.content == "hello"


def test_adapter_is_abstract():
    """LLMAdapter cannot be instantiated directly."""
    import pytest
    with pytest.raises(TypeError):
        LLMAdapter()
