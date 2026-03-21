from __future__ import annotations

import logging
from collections import defaultdict

from app.domain.models import CategoryBreakdown, DashboardResponse, MonthlySpending
from app.infrastructure.repositories.transaction_repository import TransactionRepository

logger = logging.getLogger(__name__)


class DashboardService:
    def __init__(self, txn_repo: TransactionRepository):
        self._txn_repo = txn_repo

    def get_dashboard(self, user_id: str) -> DashboardResponse:
        transactions = self._txn_repo.get_by_user(user_id)

        if not transactions:
            return DashboardResponse(
                total_spending=0.0,
                transaction_count=0,
                monthly_spending=[],
                category_breakdown=[],
            )

        total = 0.0
        category_totals: dict[str, float] = defaultdict(float)
        category_counts: dict[str, int] = defaultdict(int)
        monthly_data: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        monthly_category_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

        for txn in transactions:
            amount = abs(float(txn.amount))
            cat = txn.category.value if hasattr(txn.category, "value") else str(txn.category)
            month = txn.date[:7]  # YYYY-MM

            total += amount
            category_totals[cat] += amount
            category_counts[cat] += 1
            monthly_data[month][cat] += amount
            monthly_category_counts[month][cat] += 1

        # Build category breakdown
        category_breakdown = [
            CategoryBreakdown(
                category=cat,
                total=round(cat_total, 2),
                count=category_counts[cat],
                percentage=round((cat_total / total) * 100, 1) if total > 0 else 0.0,
            )
            for cat, cat_total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        ]

        # Build monthly spending
        monthly_spending = []
        for month in sorted(monthly_data.keys()):
            month_total = sum(monthly_data[month].values())
            month_categories = [
                CategoryBreakdown(
                    category=cat,
                    total=round(cat_total, 2),
                    count=monthly_category_counts[month][cat],
                    percentage=round((cat_total / month_total) * 100, 1) if month_total > 0 else 0.0,
                )
                for cat, cat_total in sorted(monthly_data[month].items(), key=lambda x: x[1], reverse=True)
            ]
            monthly_spending.append(MonthlySpending(
                month=month,
                total=round(month_total, 2),
                categories=month_categories,
            ))

        return DashboardResponse(
            total_spending=round(total, 2),
            transaction_count=len(transactions),
            monthly_spending=monthly_spending,
            category_breakdown=category_breakdown,
        )
