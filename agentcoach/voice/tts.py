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


class QwenTTS(TTSEngine):
    """Qwen3-TTS engine — high quality local TTS with voice cloning."""

    def __init__(self, model_name: str = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
                 device: str = "mps", speaker: str = "Vivian", lazy: bool = False):
        self.model_name = model_name
        self.device = device
        self.speaker = speaker
        self.model = None
        if not lazy:
            self._load_model()

    def _load_model(self):
        try:
            from qwen_tts import Qwen3TTSModel
            self.model = Qwen3TTSModel.from_pretrained(
                self.model_name, device_map=self.device
            )
        except ImportError:
            print("Warning: qwen-tts not installed. Run: pip install qwen-tts")
            raise

    def speak(self, text: str) -> None:
        if self.model is None:
            self._load_model()
        import tempfile
        import os
        wavs, sr = self.model.generate_custom_voice(
            text=text, language="English", speaker=self.speaker
        )
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            tmp_path = f.name
        try:
            import soundfile as sf
            sf.write(tmp_path, wavs[0].cpu().numpy(), sr)
        except ImportError:
            # Fallback: use scipy
            from scipy.io import wavfile
            import numpy as np
            wavfile.write(tmp_path, sr, (wavs[0].cpu().numpy() * 32767).astype(np.int16))
        subprocess.run(["afplay", tmp_path], check=False)
        os.unlink(tmp_path)
