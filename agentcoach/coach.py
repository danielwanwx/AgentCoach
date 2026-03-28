from agentcoach.llm.base import LLMAdapter, Message
from agentcoach.prompt.templates import get_coach_system_prompt


class Coach:
    def __init__(self, llm: LLMAdapter, mode: str = "behavioral"):
        self.llm = llm
        self.mode = mode
        system_prompt = get_coach_system_prompt(mode)
        self.history: list = [Message(role="system", content=system_prompt)]

    def start(self) -> str:
        """Start the interview session. Returns coach's opening message."""
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        return response

    def respond(self, user_input: str) -> str:
        """Send user's answer, get coach's next question/feedback."""
        self.history.append(Message(role="user", content=user_input))
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        return response
