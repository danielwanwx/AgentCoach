"""Quiz evaluator — structured assessment of user answers.

Replaces regex-based "correct"/"incorrect" pattern matching with
LLM-based evaluation. Can use a cheap/fast model (GPT-4o-mini) for
real-time evaluation, or fall back to pattern matching when no
dedicated evaluator model is available.
"""
import re
from typing import Optional

from agentcoach.llm.base import LLMAdapter, LLMProvider, Message


# Lightweight prompt for evaluating a single answer
EVAL_PROMPT = """The coach asked a question and the user answered. Was the answer correct?

Coach's response (contains the question AND evaluation):
{coach_response}

Return ONLY one word: "correct", "incorrect", or "unclear".
"""


def evaluate_answer_with_llm(
    llm: LLMAdapter,
    coach_response: str,
) -> Optional[dict]:
    """Use LLM to evaluate if the coach judged the answer correct or incorrect.

    Returns: {"is_correct": bool, "score": float} or None if can't determine.
    """
    # First try structured output if provider supports it
    if isinstance(llm, LLMProvider) and llm.supports_structured_output:
        try:
            result = llm.generate_structured(
                [Message(role="user", content=EVAL_PROMPT.format(coach_response=coach_response[:500]))],
                schema={"type": "object", "properties": {
                    "verdict": {"type": "string", "enum": ["correct", "incorrect", "unclear"]},
                }},
            )
            verdict = result.get("verdict", "unclear")
            if verdict == "correct":
                return {"is_correct": True, "score": 0.9}
            elif verdict == "incorrect":
                return {"is_correct": False, "score": 0.2}
            return None
        except Exception:
            pass

    # Fallback: use generate() and parse
    try:
        result = llm.generate(
            [Message(role="user", content=EVAL_PROMPT.format(coach_response=coach_response[:500]))]
        )
        lower = result.strip().lower()
        if "correct" in lower and "incorrect" not in lower:
            return {"is_correct": True, "score": 0.9}
        elif "incorrect" in lower:
            return {"is_correct": False, "score": 0.2}
    except Exception:
        pass

    return None


# ── Pattern-based fallback (current system) ────────────────────

_CORRECT_PATTERNS = re.compile(
    r"\*{0,2}correct\*{0,2}|✓|\bexactly\b|\bgreat answer\b|\bwell done\b|\bspot on\b|\bnailed it\b|\bthat.s right\b",
    re.IGNORECASE,
)
_INCORRECT_PATTERNS = re.compile(
    r"\*{0,2}incorrect\*{0,2}|✗|\bnot quite\b|\bwrong\b|\bnot exactly\b"
    r"|\bmissed\b|\bactually\b.*\bshould\b|\bslightly off\b|\bclose but\b"
    r"|\bnot quite right\b|\boff on\b|\bmixed.{0,15}up\b",
    re.IGNORECASE,
)

_QUIZ_START_PATTERNS = re.compile(
    r"\bquiz\b|\bquestion\s*[1-9#]|\blet.s test\b|\btest your\b|\bready.*quiz\b|\bstart.*quiz\b",
    re.IGNORECASE,
)


def evaluate_answer_with_patterns(coach_response: str) -> Optional[dict]:
    """Regex-based evaluation of coach response (fast, no LLM call).

    Returns: {"is_correct": bool, "score": float} or None.
    """
    head = coach_response[:200]
    is_correct = bool(_CORRECT_PATTERNS.search(head))
    is_incorrect = bool(_INCORRECT_PATTERNS.search(head))

    if is_correct and not is_incorrect:
        return {"is_correct": True, "score": 0.8}
    elif is_incorrect:
        return {"is_correct": False, "score": 0.2}
    return None


def detect_quiz_start(coach_response: str) -> bool:
    """Detect if coach is starting a quiz."""
    return bool(_QUIZ_START_PATTERNS.search(coach_response))
