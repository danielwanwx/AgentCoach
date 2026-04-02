"""Teaching strategies — adaptive pedagogy based on user state.

The strategy selector reads user signals (mastery, consecutive errors,
engagement level) and picks the best teaching approach for the next turn.
Each strategy has a prompt fragment that gets injected into the Coach's
system prompt, shaping HOW it responds without changing WHAT it teaches.
"""
from enum import Enum


class TeachingStrategy(Enum):
    DIRECT = "direct"           # Explain clearly. Good for first exposure.
    SOCRATIC = "socratic"       # Ask questions to guide discovery. Good for reinforcement.
    CASE_STUDY = "case_study"   # Use a real-world example. Good for application.
    ANALOGY = "analogy"         # Relate to something the user already knows. Good for confusion.
    SCAFFOLDING = "scaffolding" # Build up step by step. Good for beginners.


# Prompt fragments for each strategy
STRATEGY_PROMPTS = {
    TeachingStrategy.DIRECT: (
        "For this response, EXPLAIN the concept directly and clearly. "
        "Give a concise definition, then one concrete example. "
        "End by asking if the user has questions."
    ),
    TeachingStrategy.SOCRATIC: (
        "For this response, DO NOT explain directly. Instead, ask a guiding question "
        "that helps the user discover the answer themselves. If they're close, "
        "ask 'why do you think that?' If they're stuck, give ONE hint and ask again. "
        "The goal is for THEM to say the answer, not you."
    ),
    TeachingStrategy.CASE_STUDY: (
        "For this response, use a REAL-WORLD EXAMPLE to illustrate the concept. "
        "Describe a scenario (e.g., 'Imagine you're building Netflix's recommendation system...') "
        "then ask the user what they would do. Connect their answer to the concept."
    ),
    TeachingStrategy.ANALOGY: (
        "For this response, use an ANALOGY from everyday life to explain the concept. "
        "The user seems confused, so avoid technical jargon. "
        "Compare the concept to something familiar (cooking, driving, library, etc.). "
        "Then check: 'Does this analogy help, or should I try a different angle?'"
    ),
    TeachingStrategy.SCAFFOLDING: (
        "For this response, BREAK DOWN the concept into the simplest possible step. "
        "Start from what the user already understands and add exactly ONE new idea. "
        "Don't overwhelm with details. Confirm understanding before moving forward. "
        "Think of it as building blocks — one at a time."
    ),
}


def select_strategy(
    mode: str,
    topic_mastery: float,
    consecutive_wrong: int = 0,
    consecutive_right: int = 0,
    turn_number: int = 0,
    user_said_confused: bool = False,
) -> TeachingStrategy:
    """Select the best teaching strategy based on user state.

    Args:
        mode: "learn", "reinforce", or "mock"
        topic_mastery: 0.0 - 1.0 (from analytics)
        consecutive_wrong: how many wrong answers in a row
        consecutive_right: how many right answers in a row
        turn_number: current turn in the session
        user_said_confused: whether user expressed confusion
    """
    # Mock mode doesn't use teaching strategies
    if mode == "mock":
        return TeachingStrategy.DIRECT

    # User is confused → switch to analogy
    if user_said_confused or consecutive_wrong >= 2:
        return TeachingStrategy.ANALOGY

    # Complete beginner → scaffolding
    if topic_mastery < 0.2 and turn_number < 4:
        return TeachingStrategy.SCAFFOLDING

    # Learning phase, early turns → direct explanation
    if mode == "learn" and turn_number < 3:
        return TeachingStrategy.DIRECT

    # Reinforcement or mid-session → Socratic
    if mode == "reinforce" or (mode == "learn" and topic_mastery > 0.3):
        return TeachingStrategy.SOCRATIC

    # User is doing well → case study for deeper application
    if consecutive_right >= 2:
        return TeachingStrategy.CASE_STUDY

    # Default
    return TeachingStrategy.DIRECT


def get_strategy_prompt(strategy: TeachingStrategy) -> str:
    """Get the prompt fragment for a teaching strategy."""
    return STRATEGY_PROMPTS.get(strategy, STRATEGY_PROMPTS[TeachingStrategy.DIRECT])


# Confusion detection patterns
_CONFUSION_WORDS = [
    "confused", "don't understand", "don't get it", "lost", "what do you mean",
    "huh", "i'm not sure", "can you explain again", "what does that mean",
    "i have no idea", "that doesn't make sense", "wait what",
]


def detect_confusion(user_text: str) -> bool:
    """Detect if the user is expressing confusion."""
    lower = user_text.lower()
    return any(phrase in lower for phrase in _CONFUSION_WORDS)
