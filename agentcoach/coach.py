from agentcoach.llm.base import LLMAdapter, Message
from agentcoach.prompt.templates import build_system_prompt


class Coach:
    def __init__(self, llm: LLMAdapter, mode: str = "behavioral", memory_context: str = ""):
        self.llm = llm
        self.mode = mode
        system_prompt = build_system_prompt(mode, memory_context)
        self.history: list = [Message(role="system", content=system_prompt)]

    def start(self) -> str:
        """Start the interview session. Returns coach's opening message."""
        self.history.append(Message(role="user", content="Hi, I'm ready to start the mock interview. Please begin."))
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        return response

    def respond(self, user_input: str) -> str:
        """Send user's answer, get coach's next question/feedback."""
        self.history.append(Message(role="user", content=user_input))
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        return response

    def get_feedback_summary(self) -> str:
        """Ask the LLM to summarize the session with strengths/weaknesses."""
        if len(self.history) < 5:  # need system + start + assistant + at least one real exchange
            return ""
        self.history.append(Message(
            role="user",
            content="Please provide a brief summary of this interview session. Include: 1) Key strengths demonstrated, 2) Areas for improvement, 3) Overall score out of 10. Be specific and actionable."
        ))
        response = self.llm.generate(self.history)
        return response
