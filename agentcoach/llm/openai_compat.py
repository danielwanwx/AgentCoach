"""OpenAI-compatible LLM adapter — works with MiniMax, DeepSeek, OpenAI, etc."""
import re
import time
import openai
from agentcoach.llm.base import LLMAdapter, Message


def _strip_think_tags(text: str) -> str:
    """Strip <think>...</think> blocks from reasoning model output."""
    return re.sub(r"<think>[\s\S]*?</think>\s*", "", text).strip()

_MAX_RETRIES = 3
_RETRY_DELAY = 2


PROVIDERS = {
    "minimax": ("https://api.minimax.chat/v1", "MiniMax-M2.7"),
    "deepseek": ("https://api.deepseek.com/v1", "deepseek-chat"),
    "openai": (None, "gpt-4o-mini"),
}


class OpenAICompatAdapter(LLMAdapter):
    def __init__(self, api_key: str, provider: str = "minimax", model: str = ""):
        if provider in PROVIDERS:
            base_url, default_model = PROVIDERS[provider]
        else:
            base_url, default_model = None, "gpt-4o-mini"

        self.model_name = model or default_model
        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = openai.OpenAI(**kwargs)

    def generate(self, messages: list) -> str:
        api_messages = []
        for msg in messages:
            role = msg.role if msg.role != "assistant" else "assistant"
            api_messages.append({"role": role, "content": msg.content})

        for attempt in range(_MAX_RETRIES):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=api_messages,
                )
                text = resp.choices[0].message.content or ""
                return _strip_think_tags(text)
            except openai.RateLimitError:
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_RETRY_DELAY * (attempt + 1))
                else:
                    raise
        return ""
