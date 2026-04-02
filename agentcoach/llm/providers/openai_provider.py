"""OpenAI provider — GPT-4o, GPT-4o-mini with structured output support."""
import json
import time
import openai
from agentcoach.llm.base import LLMProvider

_MAX_RETRIES = 3
_RETRY_DELAY = 2


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.model_name = model
        self.client = openai.OpenAI(api_key=api_key)

    @property
    def name(self) -> str:
        return f"openai/{self.model_name}"

    @property
    def supports_structured_output(self) -> bool:
        return True

    def generate(self, messages: list) -> str:
        api_messages = [{"role": m.role, "content": m.content} for m in messages]
        for attempt in range(_MAX_RETRIES):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model_name, messages=api_messages,
                )
                if not resp.choices:
                    if attempt < _MAX_RETRIES - 1:
                        time.sleep(_RETRY_DELAY * (2 ** attempt))
                        continue
                    return ""
                return resp.choices[0].message.content or ""
            except (openai.RateLimitError, openai.InternalServerError, openai.APITimeoutError):
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_RETRY_DELAY * (2 ** attempt))
                else:
                    raise
        return ""

    def generate_structured(self, messages: list, schema: dict) -> dict:
        api_messages = [{"role": m.role, "content": m.content} for m in messages]
        for attempt in range(_MAX_RETRIES):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model_name, messages=api_messages,
                    response_format={"type": "json_object"},
                )
                if resp.choices:
                    return json.loads(resp.choices[0].message.content or "{}")
                return {}
            except (openai.RateLimitError, openai.InternalServerError):
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_RETRY_DELAY * (2 ** attempt))
                else:
                    raise
        return {}
