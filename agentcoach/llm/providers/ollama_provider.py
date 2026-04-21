"""Ollama native provider.

Talks to Ollama's ``/api/chat`` endpoint directly so we can pass
``think: false`` for "thinking" models such as Gemma 4. The OpenAI-compatible
endpoint cannot disable the reasoning trace, which silently consumes the
``max_tokens`` budget and returns empty content on short replies.

Set ``OLLAMA_THINK=1`` to re-enable reasoning (for debugging).
"""
from __future__ import annotations

import json
import os
import time
from typing import Any

import urllib.request
import urllib.error

from agentcoach.llm.base import LLMProvider


_DEFAULT_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
_DEFAULT_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "180"))
_MAX_RETRIES = 2
_RETRY_DELAY = 1.0


class OllamaProvider(LLMProvider):
    """Ollama chat completions via ``/api/chat``.

    Parameters
    ----------
    model: Ollama model tag (e.g. ``gemma4:31b``, ``gemma4:e4b``).
    base_url: Ollama server base URL.
    num_predict: soft token cap for the visible response. Defaults to 512,
        which is enough for any spoken coach turn.
    temperature: sampling temperature.
    think: if ``False``, Gemma-4 / reasoning models skip their thinking
        trace and spend the whole budget on the user-visible reply.
    """

    def __init__(
        self,
        model: str = "gemma4:31b",
        base_url: str = _DEFAULT_URL,
        num_predict: int = 512,
        temperature: float = 0.7,
        think: bool | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
    ):
        self.model_name = model
        self._url = base_url.rstrip("/") + "/api/chat"
        self._num_predict = num_predict
        self._temperature = temperature
        # Default to False so that reasoning models do not silently eat the
        # budget. Allow opt-in via env var for debugging.
        if think is None:
            think = os.getenv("OLLAMA_THINK", "0") == "1"
        self._think = think
        self._timeout = timeout

    @property
    def name(self) -> str:
        return f"ollama/{self.model_name}"

    @property
    def supports_structured_output(self) -> bool:
        return False

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self._url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self._timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        return json.loads(body)

    def generate(self, messages: list) -> str:
        api_messages = [{"role": m.role, "content": m.content} for m in messages]
        payload = {
            "model": self.model_name,
            "messages": api_messages,
            "stream": False,
            "think": self._think,
            "options": {
                "temperature": self._temperature,
                "num_predict": self._num_predict,
            },
        }
        last_err: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            try:
                body = self._post(payload)
                content = (body.get("message") or {}).get("content") or ""
                if content.strip():
                    return content
                # Empty content is possible if the model emitted only a
                # thinking trace. Retry once with thinking forced off.
                payload["think"] = False
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
                last_err = exc
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_RETRY_DELAY * (2 ** attempt))
                    continue
                raise
        if last_err:
            raise last_err
        return ""

    def generate_structured(self, messages: list, schema: dict) -> dict:
        # Ollama supports JSON mode via ``format: "json"``. Best-effort.
        api_messages = [{"role": m.role, "content": m.content} for m in messages]
        payload = {
            "model": self.model_name,
            "messages": api_messages,
            "stream": False,
            "think": self._think,
            "format": "json",
            "options": {
                "temperature": self._temperature,
                "num_predict": self._num_predict,
            },
        }
        body = self._post(payload)
        content = (body.get("message") or {}).get("content") or "{}"
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}
