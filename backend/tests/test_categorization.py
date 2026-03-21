import pytest

from app.domain.enums import TransactionCategory
from app.domain.models import CategorizationResult
from app.services.categorization_service import CategorizationService
from tests.conftest import MockLLMProvider


class TestRuleBasedCategorization:
    """Tests for rule-based fallback (no LLM)."""

    @pytest.fixture
    def service(self):
        return CategorizationService(llm_provider=None)

    @pytest.mark.asyncio
    async def test_food_category(self, service: CategorizationService):
        result = await service.categorize("STARBUCKS COFFEE #1234", 5.50)
        assert result.category == TransactionCategory.FOOD

    @pytest.mark.asyncio
    async def test_groceries_category(self, service: CategorizationService):
        result = await service.categorize("WALMART SUPERCENTER", 87.32)
        assert result.category == TransactionCategory.GROCERIES

    @pytest.mark.asyncio
    async def test_travel_category(self, service: CategorizationService):
        result = await service.categorize("DELTA AIRLINES", 350.00)
        assert result.category == TransactionCategory.TRAVEL

    @pytest.mark.asyncio
    async def test_bills_category(self, service: CategorizationService):
        result = await service.categorize("VERIZON WIRELESS BILL", 85.00)
        assert result.category == TransactionCategory.BILLS

    @pytest.mark.asyncio
    async def test_entertainment_category(self, service: CategorizationService):
        result = await service.categorize("NETFLIX SUBSCRIPTION", 15.99)
        assert result.category == TransactionCategory.ENTERTAINMENT

    @pytest.mark.asyncio
    async def test_shopping_category(self, service: CategorizationService):
        result = await service.categorize("AMAZON.COM PURCHASE", 42.99)
        assert result.category == TransactionCategory.SHOPPING

    @pytest.mark.asyncio
    async def test_unknown_defaults_to_other(self, service: CategorizationService):
        result = await service.categorize("MISC PAYMENT XYZ123", 100.00)
        assert result.category == TransactionCategory.OTHER

    @pytest.mark.asyncio
    async def test_batch_categorization(self, service: CategorizationService):
        items = [
            ("Starbucks", 5.00),
            ("Walmart", 50.00),
            ("Unknown XYZ", 10.00),
        ]
        results = await service.categorize_batch(items)
        assert len(results) == 3
        assert results[0].category == TransactionCategory.FOOD
        assert results[1].category == TransactionCategory.GROCERIES
        assert results[2].category == TransactionCategory.OTHER


class TestLLMCategorization:
    """Tests using mock LLM provider."""

    @pytest.mark.asyncio
    async def test_llm_called(self, mock_llm: MockLLMProvider):
        service = CategorizationService(llm_provider=mock_llm)
        result = await service.categorize("Test Transaction", 10.00)
        assert result.category == TransactionCategory.FOOD  # mock always returns FOOD
        assert len(mock_llm.calls) == 1

    @pytest.mark.asyncio
    async def test_llm_batch(self, mock_llm: MockLLMProvider):
        service = CategorizationService(llm_provider=mock_llm)
        items = [("A", 1.0), ("B", 2.0), ("C", 3.0)]
        results = await service.categorize_batch(items)
        assert len(results) == 3
        assert len(mock_llm.calls) == 3
