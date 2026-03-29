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

import time
from agentcoach.voice.tts import AsyncTTSWrapper, MacOSTTS

def test_async_tts_wrapper_non_blocking():
    """AsyncTTSWrapper returns immediately while speech plays in background."""
    mock_engine = MagicMock(spec=MacOSTTS)
    # Make speak() take some time
    def slow_speak(text):
        import time
        time.sleep(0.5)
    mock_engine.speak.side_effect = slow_speak

    wrapper = AsyncTTSWrapper(mock_engine)
    start = time.time()
    wrapper.speak("Hello")
    elapsed = time.time() - start

    # Should return almost immediately (< 0.1s), not wait 0.5s
    assert elapsed < 0.2
    # Wait for background thread to finish
    time.sleep(0.7)
    mock_engine.speak.assert_called_once_with("Hello")
