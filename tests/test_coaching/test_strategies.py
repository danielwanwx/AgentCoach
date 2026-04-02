"""Tests for agentcoach/coaching/strategies.py"""
import pytest

from agentcoach.coaching.strategies import (
    TeachingStrategy,
    select_strategy,
    get_strategy_prompt,
    detect_confusion,
    STRATEGY_PROMPTS,
)


class TestSelectStrategy:
    """Tests for the select_strategy function."""

    def test_select_scaffolding_for_beginner(self):
        """A beginner (mastery < 0.2, early turns) gets SCAFFOLDING."""
        result = select_strategy(
            mode="learn",
            topic_mastery=0.1,
            turn_number=1,
        )
        assert result == TeachingStrategy.SCAFFOLDING

    def test_select_socratic_for_medium_mastery(self):
        """Mid-mastery in learn mode triggers SOCRATIC questioning."""
        result = select_strategy(
            mode="learn",
            topic_mastery=0.5,
            turn_number=5,
        )
        assert result == TeachingStrategy.SOCRATIC

    def test_select_socratic_for_reinforce_mode(self):
        """Reinforce mode defaults to SOCRATIC."""
        result = select_strategy(
            mode="reinforce",
            topic_mastery=0.5,
            turn_number=5,
        )
        assert result == TeachingStrategy.SOCRATIC

    def test_select_analogy_when_confused(self):
        """User expressing confusion triggers ANALOGY strategy."""
        result = select_strategy(
            mode="learn",
            topic_mastery=0.5,
            user_said_confused=True,
            turn_number=5,
        )
        assert result == TeachingStrategy.ANALOGY

    def test_select_analogy_after_consecutive_wrong(self):
        """Two or more consecutive wrong answers triggers ANALOGY."""
        result = select_strategy(
            mode="learn",
            topic_mastery=0.5,
            consecutive_wrong=2,
            turn_number=5,
        )
        assert result == TeachingStrategy.ANALOGY

    def test_select_direct_for_mock_mode(self):
        """Mock mode always returns DIRECT regardless of other signals."""
        result = select_strategy(
            mode="mock",
            topic_mastery=0.1,
            consecutive_wrong=5,
            user_said_confused=True,
        )
        assert result == TeachingStrategy.DIRECT

    def test_direct_for_early_learn_turns(self):
        """Early turns in learn mode with non-beginner mastery get DIRECT."""
        result = select_strategy(
            mode="learn",
            topic_mastery=0.25,
            turn_number=1,
        )
        assert result == TeachingStrategy.DIRECT


class TestDetectConfusion:
    """Tests for confusion detection."""

    def test_detect_confusion_positive(self):
        """Phrases like 'I don't understand' are detected as confusion."""
        assert detect_confusion("I don't understand what you mean") is True
        assert detect_confusion("I'm confused about this topic") is True
        assert detect_confusion("huh") is True
        assert detect_confusion("can you explain again please") is True
        assert detect_confusion("that doesn't make sense to me") is True
        assert detect_confusion("wait what") is True

    def test_detect_confusion_negative(self):
        """Normal statements are NOT detected as confusion."""
        assert detect_confusion("I think the answer is B") is False
        assert detect_confusion("Let me try again") is False
        assert detect_confusion("The time complexity is O(n)") is False
        assert detect_confusion("Yes, I understand now") is False


class TestGetStrategyPrompt:
    """Tests for the get_strategy_prompt helper."""

    def test_get_strategy_prompt_returns_string(self):
        """Each strategy maps to a non-empty prompt string."""
        for strategy in TeachingStrategy:
            prompt = get_strategy_prompt(strategy)
            assert isinstance(prompt, str)
            assert len(prompt) > 10

    def test_get_strategy_prompt_content(self):
        """Spot-check that prompts contain key instructional phrases."""
        assert "EXPLAIN" in get_strategy_prompt(TeachingStrategy.DIRECT)
        assert "guiding question" in get_strategy_prompt(TeachingStrategy.SOCRATIC)
        assert "ANALOGY" in get_strategy_prompt(TeachingStrategy.ANALOGY)
        assert "BREAK DOWN" in get_strategy_prompt(TeachingStrategy.SCAFFOLDING)
        assert "REAL-WORLD EXAMPLE" in get_strategy_prompt(TeachingStrategy.CASE_STUDY)
