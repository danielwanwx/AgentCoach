"""Tests for agentcoach/coaching/quiz_evaluator.py"""
import pytest
from unittest.mock import MagicMock, patch

from agentcoach.coaching.quiz_evaluator import (
    evaluate_answer_with_llm,
    evaluate_answer_with_patterns,
    detect_quiz_start,
)
from agentcoach.llm.base import LLMAdapter, LLMProvider, Message


class TestEvaluateAnswerWithPatterns:
    """Tests for the regex-based pattern evaluator."""

    def test_evaluate_correct_answer(self):
        """Coach responses containing 'correct' are detected as correct."""
        result = evaluate_answer_with_patterns("Correct! That's exactly right.")
        assert result is not None
        assert result["is_correct"] is True
        assert result["score"] > 0.5

    def test_evaluate_correct_well_done(self):
        """'Well done' is also a correct signal."""
        result = evaluate_answer_with_patterns("Well done! You nailed it.")
        assert result is not None
        assert result["is_correct"] is True

    def test_evaluate_incorrect_answer(self):
        """Coach responses containing 'incorrect' are detected as wrong."""
        result = evaluate_answer_with_patterns(
            "Incorrect. The answer should be O(n log n)."
        )
        assert result is not None
        assert result["is_correct"] is False
        assert result["score"] < 0.5

    def test_evaluate_incorrect_not_quite(self):
        """'Not quite' is an incorrect signal."""
        result = evaluate_answer_with_patterns(
            "Not quite. Think about the edge case when n=0."
        )
        assert result is not None
        assert result["is_correct"] is False

    def test_evaluate_ambiguous_returns_none(self):
        """Coach responses with no clear verdict return None."""
        result = evaluate_answer_with_patterns(
            "Interesting approach. Can you tell me more about your reasoning?"
        )
        assert result is None

    def test_evaluate_with_markdown_formatting(self):
        """Markdown bold/italic around keywords should still match."""
        result = evaluate_answer_with_patterns("**Correct!** Great job.")
        assert result is not None
        assert result["is_correct"] is True

        result = evaluate_answer_with_patterns("**Incorrect** -- the right answer is X.")
        assert result is not None
        assert result["is_correct"] is False


class TestEvaluateAnswerWithLLM:
    """Tests for the LLM-based evaluator (mocked)."""

    def test_evaluate_correct_via_structured_output(self):
        """LLM structured output returning 'correct' verdict."""
        mock_llm = MagicMock(spec=LLMProvider)
        mock_llm.supports_structured_output = True
        mock_llm.generate_structured.return_value = {"verdict": "correct"}

        result = evaluate_answer_with_llm(mock_llm, "Correct! Nice work.")

        assert result is not None
        assert result["is_correct"] is True
        assert result["score"] == 0.9

    def test_evaluate_incorrect_via_structured_output(self):
        """LLM structured output returning 'incorrect' verdict."""
        mock_llm = MagicMock(spec=LLMProvider)
        mock_llm.supports_structured_output = True
        mock_llm.generate_structured.return_value = {"verdict": "incorrect"}

        result = evaluate_answer_with_llm(mock_llm, "Not quite right.")

        assert result is not None
        assert result["is_correct"] is False
        assert result["score"] == 0.2

    def test_evaluate_unclear_via_structured_output(self):
        """LLM returns 'unclear' -- function returns None."""
        mock_llm = MagicMock(spec=LLMProvider)
        mock_llm.supports_structured_output = True
        mock_llm.generate_structured.return_value = {"verdict": "unclear"}

        result = evaluate_answer_with_llm(mock_llm, "Tell me more about that.")

        assert result is None

    def test_evaluate_fallback_to_generate(self):
        """When structured output fails, falls back to generate() + parse."""
        mock_llm = MagicMock(spec=LLMProvider)
        mock_llm.supports_structured_output = True
        mock_llm.generate_structured.side_effect = Exception("not supported")
        mock_llm.generate.return_value = "correct"

        result = evaluate_answer_with_llm(mock_llm, "That's right!")

        assert result is not None
        assert result["is_correct"] is True

    def test_evaluate_plain_adapter_uses_generate(self):
        """Plain LLMAdapter (no structured output) uses generate() path."""
        mock_llm = MagicMock(spec=LLMAdapter)

        # isinstance check for LLMProvider will fail for plain LLMAdapter
        mock_llm.generate.return_value = "incorrect"

        result = evaluate_answer_with_llm(mock_llm, "Wrong answer feedback.")

        assert result is not None
        assert result["is_correct"] is False


class TestDetectQuizStart:
    """Tests for quiz start detection."""

    def test_detect_quiz_start_positive(self):
        """Responses that signal a quiz starting are detected."""
        assert detect_quiz_start("Let's test your knowledge! Question 1:") is True
        assert detect_quiz_start("Quiz time! Are you ready?") is True
        assert detect_quiz_start("Ready for the quiz? Here we go.") is True
        assert detect_quiz_start("Question 1: What is...") is True

    def test_detect_quiz_start_negative(self):
        """Normal teaching responses do not trigger quiz detection."""
        assert detect_quiz_start("Let me explain this concept to you.") is False
        assert detect_quiz_start("Great question. The answer is...") is False
        assert detect_quiz_start(
            "Here is a summary of what we covered today."
        ) is False
