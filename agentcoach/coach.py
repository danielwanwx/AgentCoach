# agentcoach/coach.py -- backward compatibility shim
from agentcoach.coaching.coach import Coach, strip_markdown
from agentcoach.coaching.quiz_state import QuizState

__all__ = ["Coach", "strip_markdown", "QuizState"]
