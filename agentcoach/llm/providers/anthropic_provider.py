"""Anthropic provider — Claude Sonnet, Haiku."""
import time
from agentcoach.llm.base import LLMProvider

_MAX_RETRIES = 3
_RETRY_DELAY = 2


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        import anthropic
        self.model_name = model
        self.client = anthropic.Anthropic(api_key=api_key)

    @property
    def name(self) -> str:
        return f"anthropic/{self.model_name}"

    @property
    def supports_structured_output(self) -> bool:
        return False  # Anthropic uses tool_use for structured output

    def generate(self, messages: list) -> str:
        import anthropic

        system_text = ""
        api_messages = []
        for msg in messages:
            if msg.role == "system":
                system_text += msg.content + "\n"
            else:
                api_messages.append({"role": msg.role, "content": msg.content})

        if api_messages and api_messages[0]["role"] != "user":
            api_messages.insert(0, {"role": "user", "content": "Begin."})

        for attempt in range(_MAX_RETRIES):
            try:
                kwargs = {"model": self.model_name, "max_tokens": 2048, "messages": api_messages}
                if system_text.strip():
                    kwargs["system"] = system_text.strip()
                resp = self.client.messages.create(**kwargs)
                return resp.content[0].text
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APITimeoutError):
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_RETRY_DELAY * (2 ** attempt))
                else:
                    raise
        return ""
