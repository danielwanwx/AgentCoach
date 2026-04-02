"""Gemini provider — Flash (cheap/fast) and Pro."""
import time
from agentcoach.llm.base import LLMProvider

_MAX_RETRIES = 3
_RETRY_DELAY = 2


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model_name = model
        self._genai = genai

    @property
    def name(self) -> str:
        return f"google/{self.model_name}"

    def generate(self, messages: list) -> str:
        # Convert to Gemini format
        system_text = ""
        history = []
        for msg in messages:
            if msg.role == "system":
                system_text += msg.content + "\n"
            elif msg.role == "user":
                history.append({"role": "user", "parts": [msg.content]})
            elif msg.role == "assistant":
                history.append({"role": "model", "parts": [msg.content]})

        model = self._genai.GenerativeModel(
            self.model_name,
            system_instruction=system_text.strip() if system_text else None,
        )

        for attempt in range(_MAX_RETRIES):
            try:
                chat = model.start_chat(history=history[:-1] if history else [])
                last_msg = history[-1]["parts"][0] if history else "Begin."
                response = chat.send_message(last_msg)
                return response.text
            except Exception:
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_RETRY_DELAY * (2 ** attempt))
                else:
                    raise
        return ""
