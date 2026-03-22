from __future__ import annotations

import logging
from decimal import Decimal

from boto3.dynamodb.conditions import Key

from app.config import get_settings
from app.domain.models import Transaction
from app.infrastructure.database import DynamoDBClient

logger = logging.getLogger(__name__)


class TransactionRepository:
    def __init__(self, db: DynamoDBClient):
        self._db = db
        self._table = get_settings().transactions_table

    def create(self, txn: Transaction) -> None:
        item = txn.model_dump()
        # DynamoDB requires Decimal for numbers
        item["amount"] = Decimal(str(item["amount"]))
        self._db.put_item(self._table, item)

    def create_batch(self, transactions: list[Transaction]) -> None:
        for txn in transactions:
            self.create(txn)

    def get_by_id(self, transaction_id: str) -> Transaction | None:
        item = self._db.get_item(self._table, {"transaction_id": transaction_id})
        return Transaction(**item) if item else None

    def get_by_user(self, user_id: str) -> list[Transaction]:
        items = self._db.query(
            self._table,
            index_name="user-id-index",
            key_condition=Key("user_id").eq(user_id),
        )
        return [Transaction(**item) for item in items]

    def get_by_user_and_month(self, user_id: str, year_month: str) -> list[Transaction]:
        """Get transactions for a user in a specific month (YYYY-MM)."""
        all_txns = self.get_by_user(user_id)
        return [t for t in all_txns if t.date.startswith(year_month)]

    def delete_by_file(self, file_id: str) -> None:
        """Delete all transactions associated with a file."""
        items = self._db.scan(
            self._table,
            filter_expression=Key("file_id").eq(file_id),
        )
        for item in items:
            self._db.table(self._table).delete_item(
                Key={"transaction_id": item["transaction_id"]}
            )
