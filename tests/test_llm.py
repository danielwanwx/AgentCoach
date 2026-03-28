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


from unittest.mock import patch, MagicMock
from agentcoach.llm.gemini import GeminiAdapter

def test_gemini_adapter_generate():
    """GeminiAdapter calls Gemini API and returns text."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Tell me about your experience."
    mock_model.generate_content.return_value = mock_response

    with patch("agentcoach.llm.gemini.genai") as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        adapter = GeminiAdapter(api_key="fake-key", model="gemini-2.0-flash")
        result = adapter.generate([
            Message(role="system", content="You are an interview coach."),
            Message(role="user", content="Start the interview."),
        ])

    assert result == "Tell me about your experience."
    mock_model.generate_content.assert_called_once()
