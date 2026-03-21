from __future__ import annotations

import logging

from boto3.dynamodb.conditions import Key

from app.config import get_settings
from app.domain.models import UserInDB
from app.infrastructure.database import DynamoDBClient

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db: DynamoDBClient):
        self._db = db
        self._table = get_settings().users_table

    def create(self, user: UserInDB) -> None:
        self._db.put_item(self._table, user.model_dump())

    def get_by_id(self, user_id: str) -> UserInDB | None:
        item = self._db.get_item(self._table, {"user_id": user_id})
        return UserInDB(**item) if item else None

    def get_by_email(self, email: str) -> UserInDB | None:
        items = self._db.query(
            self._table,
            index_name="email-index",
            key_condition=Key("email").eq(email),
        )
        return UserInDB(**items[0]) if items else None
