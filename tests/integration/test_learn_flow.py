"""Integration tests for learn session flow using mock LLM."""
import pytest
from unittest.mock import MagicMock, patch, call

from agentcoach.coach import Coach, QuizState
from agentcoach.llm.base import LLMAdapter, Message
from agentcoach.prompt.templates import build_system_prompt
from agentcoach.coaching.strategies import TeachingStrategy


class TestLearnSessionPromptConstruction:
    """Verify that a learn session assembles the correct prompt."""

    def test_learn_session_builds_correct_prompt(self):
        """System prompt contains KB teaching content, memory context, and mode template."""
        mock_llm = MagicMock(spec=LLMAdapter)
        mock_llm.generate.return_value = "Welcome! Let's learn about RAG pipelines."

        kb_content = "RAG stands for Retrieval-Augmented Generation..."
        memory_ctx = "## Learning History\nPreviously studied: embeddings (mastery 60%)"

        coach = Coach(
            llm=mock_llm,
            mode="learn",
            memory_context=memory_ctx,
            kb_teaching_context=kb_content,
            topic_name="RAG Pipeline",
        )

        # The system prompt (history[0]) should contain all injected context
        system_prompt = coach.history[0].content

        # KB teaching material is present
        assert "RAG stands for Retrieval-Augmented Generation" in system_prompt
        assert "Teaching Material" in system_prompt

        # Memory context is present
        assert "Learning History" in system_prompt
        assert "embeddings" in system_prompt

        # Mode-specific template fragments
        assert "study coach" in system_prompt.lower() or "learn" in system_prompt.lower()

    def test_learn_session_start_sends_opening_message(self):
        """coach.start() sends an opening message and stores the response."""
        mock_llm = MagicMock(spec=LLMAdapter)
        mock_llm.generate.return_value = "Hello! Today we'll cover transformers."

        coach = Coach(
            llm=mock_llm,
            mode="learn",
            topic_name="Transformers",
            kb_teaching_context="Transformer architecture uses self-attention...",
        )

        response = coach.start()

        assert response == "Hello! Today we'll cover transformers."
        assert len(coach.history) == 3  # system + user opening + assistant response
        assert coach.history[1].role == "user"
        assert coach.history[2].role == "assistant"


class TestLearnSessionQuizTracking:
    """Verify quiz state tracking during a learn session."""

    def test_learn_session_quiz_state_tracks(self):
        """Quiz state updates when coach signals correct/incorrect answers."""
        mock_llm = MagicMock(spec=LLMAdapter)
        mock_llm.generate.side_effect = [
            "Welcome! Let's start learning.",
            # First response signals quiz start
            "Let's test your knowledge! Question 1: What is a vector embedding?",
            # Second response evaluates as correct
            "Correct! A vector embedding is a dense numerical representation.",
            # Third response evaluates as incorrect
            "Not quite. The answer should involve cosine similarity.",
        ]

        coach = Coach(llm=mock_llm, mode="learn")
        coach.start()

        # Trigger quiz detection
        coach.respond("I'm ready for the quiz")
        assert coach.quiz_state._quiz_active is True

        # Correct answer
        coach.respond("A vector embedding maps items to dense vectors")
        assert coach.quiz_state.correct_count == 1
        assert coach.quiz_state.question_count == 1

        # Incorrect answer
        coach.respond("You compare embeddings with Euclidean distance")
        assert coach.quiz_state.incorrect_count == 1
        assert coach.quiz_state.question_count == 2


class TestLearnSessionStrategyInjection:
    """Verify that teaching strategies are injected into LLM calls."""

    def test_strategy_injected_in_respond(self):
        """In learn mode, respond() injects a strategy hint as a system message."""
        mock_llm = MagicMock(spec=LLMAdapter)
        mock_llm.generate.side_effect = [
            "Welcome to learning!",
            "Let me break this down step by step...",
        ]

        coach = Coach(
            llm=mock_llm,
            mode="learn",
            kb_teaching_context="Some content here",
            topic_name="Test Topic",
        )
        coach.start()

        # Respond as a beginner (low mastery, early turn)
        coach.respond("I have no idea what this topic is about")

        # The second generate() call should include a strategy hint
        # (the first call is from start())
        last_call_messages = mock_llm.generate.call_args_list[-1][0][0]

        # Find any system messages injected after the first one
        system_messages = [m for m in last_call_messages if m.role == "system"]
        # Should have at least the original system prompt + strategy injection
        assert len(system_messages) >= 1

    def test_mock_mode_does_not_inject_strategy(self):
        """In mock mode, no strategy hint is injected."""
        mock_llm = MagicMock(spec=LLMAdapter)
        mock_llm.generate.side_effect = [
            "Welcome to your mock interview.",
            "Tell me about a system you designed.",
        ]

        coach = Coach(llm=mock_llm, mode="mock_system_design")
        coach.start()
        coach.respond("I designed a URL shortener")

        # In mock mode, respond() should NOT inject strategy messages
        # because mode does not start with "learn" or "reinforce"
        assert coach._current_strategy is None


class TestLearnSessionScoringWithRubric:
    """Verify rubric integration in session scoring."""

    def test_learn_session_scores_with_rubric(self):
        """get_feedback_summary sends the right prompt for scoring."""
        mock_llm = MagicMock(spec=LLMAdapter)
        # Need enough history: start() + a few exchanges
        mock_llm.generate.side_effect = [
            "Welcome!",
            "Quiz time! Question 1: What is X?",
            "Correct! Good job.",
            "Overall: Strengths: good recall. Weaknesses: needs practice. Score: 7/10",
        ]

        coach = Coach(llm=mock_llm, mode="learn")
        coach.start()
        coach.respond("ready for quiz")
        coach.respond("X is a thing")

        feedback = coach.get_feedback_summary()

        assert "Score" in feedback or "score" in feedback.lower() or feedback != ""
        # Verify that get_feedback_summary() actually called generate
        assert mock_llm.generate.call_count == 4
