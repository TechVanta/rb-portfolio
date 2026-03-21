from __future__ import annotations

import abc

from app.domain.models import CategorizationRequest, CategorizationResult


class LLMProvider(abc.ABC):
    """Abstract interface for LLM-based categorization."""

    @abc.abstractmethod
    async def categorize(self, request: CategorizationRequest) -> CategorizationResult:
        """Categorize a single transaction."""

    @abc.abstractmethod
    async def categorize_batch(self, requests: list[CategorizationRequest]) -> list[CategorizationResult]:
        """Categorize a batch of transactions (default: sequential calls)."""

    def _build_prompt(self, description: str, amount: float) -> str:
        return (
            "You are a financial transaction categorizer. "
            "Classify the following transaction into EXACTLY ONE of these categories:\n"
            '["Food", "Travel", "Groceries", "Bills", "Shopping", "Entertainment", '
            '"Healthcare", "Education", "Transportation", "Other"]\n\n'
            f"Transaction description: {description}\n"
            f"Amount: ${amount:.2f}\n\n"
            "Respond ONLY with valid JSON in this exact format:\n"
            '{"category": "<category>", "confidence": <0.0-1.0>}\n'
            "Do not include any other text or explanation."
        )
