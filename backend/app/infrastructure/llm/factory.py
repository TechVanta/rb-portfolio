from __future__ import annotations

import logging

from app.config import Settings
from app.domain.exceptions import LLMProviderError

from .base import LLMProvider
from .grok_provider import GrokProvider
from .groq_provider import GroqProvider
from .openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)

_PROVIDERS: dict[str, type[LLMProvider]] = {
    "openai": OpenAIProvider,
    "grok": GrokProvider,
    "groq": GroqProvider,
}


def create_llm_provider(settings: Settings) -> LLMProvider:
    """Factory: create an LLM provider based on configuration."""
    provider_name = settings.llm_provider.lower()
    provider_cls = _PROVIDERS.get(provider_name)
    if provider_cls is None:
        raise LLMProviderError(
            provider_name,
            f"Unknown provider. Available: {list(_PROVIDERS.keys())}",
        )
    logger.info("Using LLM provider: %s", provider_name)
    return provider_cls(settings)
