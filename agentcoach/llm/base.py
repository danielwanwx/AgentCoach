"""LLM base classes — backward-compatible adapter + new provider abstraction."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Message:
    role: str  # "system", "user", "assistant"
    content: str


class LLMAdapter(ABC):
    """Original adapter interface — all existing code uses this."""

    @abstractmethod
    def generate(self, messages: list) -> str:
        """Send messages, return assistant response text."""
        ...


class LLMProvider(LLMAdapter):
    """Extended provider with structured output + metadata.

    Inherits from LLMAdapter so it works everywhere the old interface is used.
    New code can use the richer interface (structured output, model info).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name, e.g. 'openai/gpt-4o'."""
        ...

    @property
    def supports_structured_output(self) -> bool:
        """Whether this provider supports JSON schema responses."""
        return False

    def generate_structured(self, messages: list, schema: dict) -> dict:
        """Generate a response conforming to a JSON schema.

        Default: call generate() and parse JSON from response.
        Providers with native structured output should override this.
        """
        import json
        import re
        text = self.generate(messages)
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
        return {}
