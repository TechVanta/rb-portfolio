from __future__ import annotations

import json
import logging

import httpx

from app.config import Settings
from app.domain.enums import TransactionCategory
from app.domain.exceptions import LLMProviderError
from app.domain.models import CategorizationRequest, CategorizationResult

from .base import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI-compatible LLM provider."""

    def __init__(self, settings: Settings):
        self._api_key = settings.llm_api_key
        self._model = settings.openai_model
        self._base_url = "https://api.openai.com/v1"
        if not self._api_key:
            raise LLMProviderError("openai", "LLM_API_KEY is not set")

    async def categorize(self, request: CategorizationRequest) -> CategorizationResult:
        prompt = self._build_prompt(request.description, request.amount)
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self._model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.0,
                        "max_tokens": 60,
                    },
                )
                resp.raise_for_status()
                body = resp.json()

            content = body["choices"][0]["message"]["content"].strip()
            parsed = json.loads(content)
            category = TransactionCategory(parsed["category"])
            confidence = float(parsed.get("confidence", 0.0))
            return CategorizationResult(category=category, confidence=confidence)

        except (httpx.HTTPError, json.JSONDecodeError, KeyError, ValueError) as exc:
            logger.warning("OpenAI categorization failed for '%s': %s", request.description, exc)
            return CategorizationResult(category=TransactionCategory.OTHER, confidence=0.0)

    async def categorize_batch(self, requests: list[CategorizationRequest]) -> list[CategorizationResult]:
        results = []
        for req in requests:
            result = await self.categorize(req)
            results.append(result)
        return results
