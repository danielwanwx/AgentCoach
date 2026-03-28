from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    role: str  # "system", "user", "assistant"
    content: str


class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, messages: list) -> str:
        """Send messages, return assistant response text."""
        ...
