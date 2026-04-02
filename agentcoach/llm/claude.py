"""Claude LLM adapter — uses Anthropic API directly."""
import time
from agentcoach.llm.base import LLMAdapter, Message

_MAX_RETRIES = 3
_RETRY_DELAY = 2


class ClaudeAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        import anthropic
        self.model_name = model
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, messages: list) -> str:
        import anthropic

        # Separate system message from conversation
        system_text = ""
        api_messages = []
        for msg in messages:
            if msg.role == "system":
                system_text += msg.content + "\n"
            else:
                api_messages.append({"role": msg.role, "content": msg.content})

        # Ensure first message is user (Anthropic requirement)
        if api_messages and api_messages[0]["role"] != "user":
            api_messages.insert(0, {"role": "user", "content": "Begin."})

        for attempt in range(_MAX_RETRIES):
            try:
                kwargs = {
                    "model": self.model_name,
                    "max_tokens": 1024,
                    "messages": api_messages,
                }
                if system_text.strip():
                    kwargs["system"] = system_text.strip()

                resp = self.client.messages.create(**kwargs)
                return resp.content[0].text
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APITimeoutError):
                wait = _RETRY_DELAY * (2 ** attempt)
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(wait)
                else:
                    raise
        return ""
