"""LLM Router — selects the best provider for each task type.

Task routing allows using different models for different purposes:
- coaching: best quality model for teaching
- scoring: model with reliable structured output
- quiz_eval: fast/cheap model for quick evaluations
- compression: long-context model for summarization
"""
import os
from typing import Optional
from agentcoach.llm.base import LLMAdapter, LLMProvider

# Default routing: maps task → provider config key
DEFAULT_ROUTING = {
    "coaching": "default",
    "scoring": "default",
    "quiz_eval": "default",
    "compression": "default",
    "kb_rerank": "default",
}


def create_provider(provider_name: str, api_key: str, model: str = "") -> LLMAdapter:
    """Create an LLM provider by name.

    Args:
        provider_name: one of "openai", "anthropic", "gemini", "minimax", "deepseek"
        api_key: API key for the provider
        model: model name override (uses provider default if empty)
    """
    if provider_name == "openai":
        from agentcoach.llm.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(api_key=api_key, model=model or "gpt-4o-mini")
    elif provider_name == "anthropic":
        from agentcoach.llm.providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider(api_key=api_key, model=model or "claude-sonnet-4-20250514")
    elif provider_name == "gemini":
        from agentcoach.llm.providers.gemini_provider import GeminiProvider
        return GeminiProvider(api_key=api_key, model=model or "gemini-2.0-flash")
    else:
        # Fall back to OpenAI-compatible adapter (minimax, deepseek, etc.)
        from agentcoach.llm.openai_compat import OpenAICompatAdapter
        return OpenAICompatAdapter(api_key=api_key, provider=provider_name, model=model)


class LLMRouter:
    """Routes tasks to the best available LLM provider.

    Usage:
        router = LLMRouter.from_env()
        coach_llm = router.get("coaching")
        scorer_llm = router.get("scoring")
    """

    def __init__(self, default_provider: LLMAdapter, task_providers: dict = None):
        self._default = default_provider
        self._providers = task_providers or {}

    def get(self, task: str = "default") -> LLMAdapter:
        """Get the best provider for a task type."""
        return self._providers.get(task, self._default)

    @classmethod
    def from_env(cls) -> "LLMRouter":
        """Create router from environment variables.

        Env vars:
            LLM_PROVIDER: default provider name (minimax, openai, anthropic, gemini)
            LLM_API_KEY: API key for default provider
            LLM_MODEL: model override for default provider
            OPENAI_API_KEY: if set, enables OpenAI for scoring tasks
            ANTHROPIC_API_KEY: if set, enables Anthropic for coaching tasks
            GEMINI_API_KEY: if set, enables Gemini for compression tasks
        """
        # Default provider
        provider_name = os.getenv("LLM_PROVIDER", "minimax")
        api_key = os.getenv("LLM_API_KEY", "")
        model = os.getenv("LLM_MODEL", "")
        default = create_provider(provider_name, api_key, model)

        # Task-specific providers (if keys available)
        task_providers = {}

        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            task_providers["scoring"] = create_provider("openai", openai_key, "gpt-4o")
            task_providers["quiz_eval"] = create_provider("openai", openai_key, "gpt-4o-mini")

        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            task_providers["coaching"] = create_provider("anthropic", anthropic_key)

        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            task_providers["compression"] = create_provider("gemini", gemini_key)
            task_providers["kb_rerank"] = create_provider("gemini", gemini_key)

        return cls(default_provider=default, task_providers=task_providers)
