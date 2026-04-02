"""Tests for agentcoach/llm/router.py"""
import pytest
from unittest.mock import MagicMock, patch

from agentcoach.llm.router import LLMRouter, create_provider, DEFAULT_ROUTING
from agentcoach.llm.base import LLMAdapter


class TestLLMRouter:
    """Tests for the LLMRouter class."""

    def test_router_returns_default_provider(self):
        """get() with no task-specific mapping returns the default provider."""
        default = MagicMock(spec=LLMAdapter)
        router = LLMRouter(default_provider=default)

        result = router.get("coaching")

        assert result is default

    def test_router_returns_task_specific_provider(self):
        """get() returns the task-specific provider when one is registered."""
        default = MagicMock(spec=LLMAdapter)
        scoring_provider = MagicMock(spec=LLMAdapter)
        router = LLMRouter(
            default_provider=default,
            task_providers={"scoring": scoring_provider},
        )

        result = router.get("scoring")

        assert result is scoring_provider
        assert result is not default

    def test_router_falls_back_to_default_on_unknown_task(self):
        """get() with an unregistered task name falls back to the default."""
        default = MagicMock(spec=LLMAdapter)
        scoring_provider = MagicMock(spec=LLMAdapter)
        router = LLMRouter(
            default_provider=default,
            task_providers={"scoring": scoring_provider},
        )

        result = router.get("totally_unknown_task")

        assert result is default

    @patch("agentcoach.llm.router.create_provider")
    def test_router_get_default_key(self, mock_create):
        """get('default') returns the default provider."""
        default = MagicMock(spec=LLMAdapter)
        router = LLMRouter(default_provider=default)

        result = router.get("default")

        assert result is default


class TestCreateProvider:
    """Tests for the create_provider factory function."""

    @patch("agentcoach.llm.providers.openai_provider.OpenAIProvider")
    def test_create_provider_openai(self, MockOpenAI):
        """create_provider('openai', ...) returns an OpenAIProvider."""
        mock_instance = MagicMock(spec=LLMAdapter)
        MockOpenAI.return_value = mock_instance

        result = create_provider("openai", "sk-test-key", "gpt-4o")

        MockOpenAI.assert_called_once_with(api_key="sk-test-key", model="gpt-4o")
        assert result is mock_instance

    @patch("agentcoach.llm.openai_compat.OpenAICompatAdapter")
    def test_create_provider_minimax(self, MockCompat):
        """create_provider('minimax', ...) falls back to OpenAICompatAdapter."""
        mock_instance = MagicMock(spec=LLMAdapter)
        MockCompat.return_value = mock_instance

        result = create_provider("minimax", "mm-test-key", "abab-7")

        MockCompat.assert_called_once_with(
            api_key="mm-test-key", provider="minimax", model="abab-7"
        )
        assert result is mock_instance

    @patch("agentcoach.llm.providers.openai_provider.OpenAIProvider")
    def test_create_provider_openai_default_model(self, MockOpenAI):
        """create_provider('openai', ...) uses gpt-4o-mini when no model given."""
        MockOpenAI.return_value = MagicMock()

        create_provider("openai", "sk-test-key", "")

        MockOpenAI.assert_called_once_with(api_key="sk-test-key", model="gpt-4o-mini")

    @patch("agentcoach.llm.providers.anthropic_provider.AnthropicProvider")
    def test_create_provider_anthropic(self, MockAnthropic):
        """create_provider('anthropic', ...) returns an AnthropicProvider."""
        mock_instance = MagicMock()
        MockAnthropic.return_value = mock_instance

        result = create_provider("anthropic", "ant-key")

        MockAnthropic.assert_called_once_with(
            api_key="ant-key", model="claude-sonnet-4-20250514"
        )
        assert result is mock_instance

    @patch("agentcoach.llm.providers.gemini_provider.GeminiProvider")
    def test_create_provider_gemini(self, MockGemini):
        """create_provider('gemini', ...) returns a GeminiProvider."""
        mock_instance = MagicMock()
        MockGemini.return_value = mock_instance

        result = create_provider("gemini", "gem-key", "gemini-2.0-flash")

        MockGemini.assert_called_once_with(
            api_key="gem-key", model="gemini-2.0-flash"
        )
        assert result is mock_instance
