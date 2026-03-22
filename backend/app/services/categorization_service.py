from __future__ import annotations

import logging

from app.domain.enums import TransactionCategory
from app.domain.models import CategorizationRequest, CategorizationResult
from app.infrastructure.llm.base import LLMProvider

logger = logging.getLogger(__name__)

# Rule-based fallback patterns for when LLM is unavailable
_KEYWORD_RULES: dict[TransactionCategory, list[str]] = {
    TransactionCategory.FOOD: [
        "restaurant", "cafe", "coffee", "pizza", "burger", "sushi",
        "mcdonald", "starbucks", "chipotle", "subway", "doordash",
        "uber eats", "grubhub", "dining",
    ],
    TransactionCategory.GROCERIES: [
        "grocery", "supermarket", "walmart", "costco", "trader joe",
        "whole foods", "kroger", "safeway", "target", "aldi",
    ],
    TransactionCategory.TRAVEL: [
        "airline", "hotel", "airbnb", "booking.com", "expedia",
        "flight", "delta", "united", "american airlines", "marriott",
    ],
    TransactionCategory.TRANSPORTATION: [
        "uber", "lyft", "taxi", "parking", "gas station", "shell",
        "chevron", "exxon", "bp", "transit", "metro",
    ],
    TransactionCategory.BILLS: [
        "electric", "water", "internet", "phone", "insurance",
        "rent", "mortgage", "utility", "at&t", "verizon", "comcast",
    ],
    TransactionCategory.SHOPPING: [
        "amazon", "ebay", "etsy", "apple store", "best buy",
        "nordstrom", "zara", "h&m", "nike", "clothing",
    ],
    TransactionCategory.ENTERTAINMENT: [
        "netflix", "spotify", "hulu", "disney", "cinema", "movie",
        "theater", "concert", "game", "playstation", "xbox", "steam",
    ],
    TransactionCategory.HEALTHCARE: [
        "pharmacy", "hospital", "doctor", "dental", "medical",
        "cvs", "walgreens", "insurance", "health",
    ],
    TransactionCategory.EDUCATION: [
        "university", "college", "school", "tuition", "course",
        "udemy", "coursera", "textbook",
    ],
}


class CategorizationService:
    """Categorizes transactions using LLM with rule-based fallback."""

    def __init__(self, llm_provider: LLMProvider | None = None):
        self._llm = llm_provider

    async def categorize(self, description: str, amount: float) -> CategorizationResult:
        if self._llm:
            try:
                req = CategorizationRequest(description=description, amount=amount)
                return await self._llm.categorize(req)
            except Exception as exc:
                logger.warning("LLM categorization failed, falling back to rules: %s", exc)

        # Rule-based fallback
        return self._rule_based_categorize(description)

    async def categorize_batch(
        self, items: list[tuple[str, float]]
    ) -> list[CategorizationResult]:
        if self._llm:
            try:
                requests = [CategorizationRequest(description=d, amount=a) for d, a in items]
                return await self._llm.categorize_batch(requests)
            except Exception as exc:
                logger.warning("LLM batch categorization failed, falling back to rules: %s", exc)

        return [self._rule_based_categorize(desc) for desc, _ in items]

    @staticmethod
    def _rule_based_categorize(description: str) -> CategorizationResult:
        desc_lower = description.lower()
        for category, keywords in _KEYWORD_RULES.items():
            if any(kw in desc_lower for kw in keywords):
                return CategorizationResult(category=category, confidence=0.7)
        return CategorizationResult(category=TransactionCategory.OTHER, confidence=0.3)
