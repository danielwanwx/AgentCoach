from unittest.mock import patch, MagicMock
from agentcoach.voice.tts import MacOSTTS, TTSEngine
import pytest

def test_tts_engine_is_abstract():
    with pytest.raises(TypeError):
        TTSEngine()

def test_macos_tts_speak():
    tts = MacOSTTS()
    with patch("agentcoach.voice.tts.subprocess") as mock_sub:
        mock_sub.run.return_value = MagicMock(returncode=0)
        tts.speak("Hello world")
        mock_sub.run.assert_called_once()
        cmd = mock_sub.run.call_args[0][0]
        assert "say" in cmd
        assert "Hello world" in cmd

def test_macos_tts_custom_voice():
    tts = MacOSTTS(voice="Alex", rate=200)
    with patch("agentcoach.voice.tts.subprocess") as mock_sub:
        mock_sub.run.return_value = MagicMock(returncode=0)
        tts.speak("Test")
        cmd = mock_sub.run.call_args[0][0]
        assert "Alex" in cmd
        assert "200" in cmd

def test_qwen_tts_lazy_initialization():
    """QwenTTS can be instantiated with lazy loading — model not loaded until speak()."""
    from agentcoach.voice.tts import QwenTTS
    tts = QwenTTS(device="cpu", lazy=True)
    assert tts.model is None
