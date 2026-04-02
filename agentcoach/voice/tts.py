"""TTS engines — pluggable text-to-speech."""
from __future__ import annotations

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
            print("Warning: qwen-tts not installed. Run: pip install qwen-tts")  # UI output
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


class VibeVoiceTTS(TTSEngine):
    """VibeVoice 1.5B TTS — high quality with voice cloning support."""

    def __init__(
        self,
        model_path: str = "microsoft/VibeVoice-1.5B",
        device: str = "mps",
        inference_steps: int = 15,
        cfg_scale: float = 1.5,
        voice_sample: str | None = None,
        lazy: bool = False,
    ):
        self.model_path = model_path
        self.device = device
        self.inference_steps = inference_steps
        self.cfg_scale = cfg_scale
        self.voice_sample = voice_sample  # path to .wav for voice cloning
        self._service = None
        if not lazy:
            self._load()

    def _load(self):
        import torch
        from vibevoice.processor.vibevoice_processor import VibeVoiceProcessor
        from vibevoice.modular.modeling_vibevoice_inference import (
            VibeVoiceForConditionalGenerationInference,
        )

        self._processor = VibeVoiceProcessor.from_pretrained(self.model_path)
        self._model = VibeVoiceForConditionalGenerationInference.from_pretrained(
            self.model_path,
            torch_dtype=torch.bfloat16,
            device_map=self.device,
        )
        self._model.eval()
        self._loaded = True

    def speak(self, text: str) -> None:
        if not getattr(self, "_loaded", False):
            self._load()

        import tempfile
        import os
        import torch

        # Strip markdown/emoji before sending to TTS
        import re
        clean = re.sub(r'[#*_`~\[\](){}|>]', '', text)  # remove markdown chars
        clean = re.sub(r'https?://\S+', '', clean)        # remove URLs
        clean = re.sub(r'[\U0001f300-\U0001f9ff]', '', clean)  # remove emoji
        clean = re.sub(r'---+', '', clean)                # remove horizontal rules
        clean = re.sub(r'\n{2,}', '. ', clean)            # paragraph breaks → pause
        clean = re.sub(r'\n', ' ', clean)                 # remaining newlines
        clean = re.sub(r'\s{2,}', ' ', clean).strip()     # collapse whitespace

        # VibeVoice-TTS expects multi-speaker script format
        script = f"Speaker 1: {clean}"
        voice_args = {}
        if self.voice_sample:
            voice_args["voice_samples"] = [self.voice_sample]
        inputs = self._processor(text=script, **voice_args, return_tensors="pt")
        # Move tensors to device, pass non-tensors as-is
        model_inputs = {}
        for k, v in inputs.items():
            if isinstance(v, torch.Tensor):
                model_inputs[k] = v.to(self._model.device)
            elif v is not None:
                model_inputs[k] = v

        # VibeVoice generate() has a bug: calls .to() on speech_tensors even
        # when None. Provide a tiny dummy audio waveform to avoid the crash.
        if model_inputs.get("speech_tensors") is None:
            device = self._model.device
            # Dummy 1-sample silence waveform (shape: batch, samples)
            model_inputs["speech_tensors"] = torch.zeros(
                1, 3200, dtype=torch.bfloat16, device=device
            )
            model_inputs["speech_masks"] = torch.zeros(
                1, 1, dtype=torch.bool, device=device
            )

        with torch.no_grad():
            output = self._model.generate(
                **model_inputs,
                cfg_scale=self.cfg_scale,
                tokenizer=self._processor.tokenizer,
            )

        if not output.speech_outputs or output.speech_outputs[0] is None:
            return
        audio = output.speech_outputs[0][0].float().cpu().numpy()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            tmp_path = f.name
        try:
            import soundfile as sf
            sf.write(tmp_path, audio, 24000)
        except ImportError:
            from scipy.io import wavfile
            wavfile.write(tmp_path, 24000, (audio * 32767).astype(np.int16))
        subprocess.run(["afplay", tmp_path], check=False)
        os.unlink(tmp_path)


import threading


class AsyncTTSWrapper(TTSEngine):
    """Wraps any TTS engine to speak in a background thread."""

    def __init__(self, engine: TTSEngine):
        self.engine = engine
        self._thread = None

    def speak(self, text: str) -> None:
        # Wait for previous speech to finish before starting new one
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.1)
        self._thread = threading.Thread(
            target=self.engine.speak, args=(text,), daemon=True
        )
        self._thread.start()
