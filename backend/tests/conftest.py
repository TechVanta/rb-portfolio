import pytest

from app.domain.enums import TransactionCategory
from app.domain.models import CategorizationRequest, CategorizationResult
from app.infrastructure.llm.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """Deterministic mock LLM provider for testing."""

    def __init__(self, default_category: TransactionCategory = TransactionCategory.OTHER):
        self.default_category = default_category
        self.calls: list[CategorizationRequest] = []

    async def categorize(self, request: CategorizationRequest) -> CategorizationResult:
        self.calls.append(request)
        return CategorizationResult(category=self.default_category, confidence=0.95)

    async def categorize_batch(self, requests: list[CategorizationRequest]) -> list[CategorizationResult]:
        results = []
        for req in requests:
            results.append(await self.categorize(req))
        return results


@pytest.fixture
def mock_llm():
    return MockLLMProvider(TransactionCategory.FOOD)
