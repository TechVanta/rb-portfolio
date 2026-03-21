from __future__ import annotations

import logging

from boto3.dynamodb.conditions import Key

from app.config import get_settings
from app.domain.models import FileRecord
from app.infrastructure.database import DynamoDBClient

logger = logging.getLogger(__name__)


class FileRepository:
    def __init__(self, db: DynamoDBClient):
        self._db = db
        self._table = get_settings().files_table

    def create(self, record: FileRecord) -> None:
        self._db.put_item(self._table, record.model_dump())

    def get_by_id(self, file_id: str) -> FileRecord | None:
        item = self._db.get_item(self._table, {"file_id": file_id})
        return FileRecord(**item) if item else None

    def get_by_user(self, user_id: str) -> list[FileRecord]:
        items = self._db.query(
            self._table,
            index_name="user-id-index",
            key_condition=Key("user_id").eq(user_id),
        )
        return [FileRecord(**item) for item in items]

    def update_status(self, file_id: str, status: str, error_message: str | None = None, transaction_count: int = 0) -> None:
        expr_values = {
            ":s": status,
            ":tc": transaction_count,
        }
        update_expr = "SET #st = :s, transaction_count = :tc"
        expr_names = {"#st": "status"}

        if error_message:
            update_expr += ", error_message = :em"
            expr_values[":em"] = error_message

        self._db.update_item(
            self._table,
            key={"file_id": file_id},
            update_expr=update_expr,
            expr_values=expr_values,
            expr_names=expr_names,
        )
