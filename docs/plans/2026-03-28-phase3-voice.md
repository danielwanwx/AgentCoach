# Phase 3: Voice Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add voice output (TTS) so Coach speaks responses aloud. Superwhisper handles input natively (pastes into terminal).

**Architecture:** Coach response text → TTS engine → audio playback. TTS is pluggable: macOS `say` (instant, fallback) → Qwen3-TTS (high quality, local).

**Tech Stack:** macOS `say` command, Qwen3-TTS (0.6B, MPS), subprocess for audio playback

---

### Task 1: TTS Base Interface + macOS say

**Files:**
- Create: `agentcoach/voice/__init__.py`
- Create: `agentcoach/voice/tts.py`
- Create: `tests/test_tts.py`

**Step 1: Write tests**

```python
# tests/test_tts.py
from unittest.mock import patch, MagicMock
from agentcoach.voice.tts import MacOSTTS

def test_macos_tts_speak(tmp_path):
    tts = MacOSTTS()
    with patch("agentcoach.voice.tts.subprocess") as mock_sub:
        mock_sub.run.return_value = MagicMock(returncode=0)
        tts.speak("Hello world")
        mock_sub.run.assert_called_once()
        cmd = mock_sub.run.call_args[0][0]
        assert "say" in cmd
        assert "Hello world" in cmd
```

**Step 2: Write implementation**

```python
# agentcoach/voice/__init__.py
```

```python
# agentcoach/voice/tts.py
"""TTS engines — pluggable text-to-speech."""
import subprocess
from abc import ABC, abstractmethod


class TTSEngine(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        ...


class MacOSTTS(TTSEngine):
    def __init__(self, voice: str = "Samantha", rate: int = 180):
        self.voice = voice
        self.rate = rate

    def speak(self, text: str) -> None:
        subprocess.run(
            ["say", "-v", self.voice, "-r", str(self.rate), text],
            check=False,
        )
```

**Step 3: Run tests, commit**

```bash
git add agentcoach/voice/ tests/test_tts.py
git commit -m "feat: add TTS base interface and macOS say engine"
```

---

### Task 2: Qwen3-TTS Engine

**Files:**
- Modify: `agentcoach/voice/tts.py` — add QwenTTS class
- Modify: `tests/test_tts.py`

**Step 1: Write test**

```python
def test_qwen_tts_initialization():
    """QwenTTS can be imported and instantiated (model loading is lazy)."""
    from agentcoach.voice.tts import QwenTTS
    tts = QwenTTS(device="cpu", lazy=True)
    assert tts.model is None  # not loaded yet
```

**Step 2: Implement QwenTTS**

```python
class QwenTTS(TTSEngine):
    def __init__(self, model_name: str = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
                 device: str = "mps", speaker: str = "Vivian", lazy: bool = False):
        self.model_name = model_name
        self.device = device
        self.speaker = speaker
        self.model = None
        if not lazy:
            self._load_model()

    def _load_model(self):
        from qwen_tts import Qwen3TTSModel
        self.model = Qwen3TTSModel.from_pretrained(
            self.model_name, device_map=self.device
        )

    def speak(self, text: str) -> None:
        if self.model is None:
            self._load_model()
        import soundfile as sf
        import tempfile
        import subprocess
        wavs, sr = self.model.generate_custom_voice(
            text=text, language="English", speaker=self.speaker
        )
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            sf.write(f.name, wavs[0].cpu().numpy(), sr)
            subprocess.run(["afplay", f.name], check=False)
```

**Step 3: Run tests, commit**

```bash
git add agentcoach/voice/tts.py tests/test_tts.py
git commit -m "feat: add Qwen3-TTS engine with MPS support"
```

---

### Task 3: Wire TTS into CLI

**Files:**
- Modify: `agentcoach/cli.py`

**Step 1: Add TTS configuration via env vars**

- `TTS_ENGINE=macos` (default) or `TTS_ENGINE=qwen` or `TTS_ENGINE=none`
- `TTS_VOICE=Samantha` (for macOS)

**Step 2: After each `coach.respond()` and `coach.start()`, call `tts.speak(response)`**

**Step 3: Add `voice on/off` toggle command in CLI**

**Step 4: Run all tests, commit**

```bash
git add agentcoach/cli.py
git commit -m "feat: wire TTS into CLI with engine selection"
```

---

### Task 4: Async TTS (Non-Blocking)

**Files:**
- Modify: `agentcoach/voice/tts.py`

**Step 1: Add async speak**

TTS should not block the main loop. Use threading to play audio in background.

```python
import threading

class AsyncTTSWrapper(TTSEngine):
    def __init__(self, engine: TTSEngine):
        self.engine = engine
        self._thread = None

    def speak(self, text: str) -> None:
        if self._thread and self._thread.is_alive():
            pass  # skip if still speaking
        self._thread = threading.Thread(target=self.engine.speak, args=(text,), daemon=True)
        self._thread.start()
```

**Step 2: Run tests, commit**

```bash
git add agentcoach/voice/tts.py
git commit -m "feat: add async TTS wrapper for non-blocking speech"
```

---

### Task 5: Run All Tests + Tag

**Step 1:** `python3 -m pytest tests/ -v`
**Step 2:** `git tag v0.3.0-phase3`
