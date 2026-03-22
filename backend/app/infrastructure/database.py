from __future__ import annotations

import logging
from typing import Any

import boto3
from botocore.config import Config

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


def _get_boto_kwargs(settings: Settings) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"region_name": settings.aws_region}
    if settings.aws_access_key_id:
        kwargs["aws_access_key_id"] = settings.aws_access_key_id
        kwargs["aws_secret_access_key"] = settings.aws_secret_access_key
    return kwargs


class DynamoDBClient:
    """Thin wrapper around boto3 DynamoDB resource."""

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        kwargs = _get_boto_kwargs(self._settings)
        if self._settings.dynamodb_endpoint:
            kwargs["endpoint_url"] = self._settings.dynamodb_endpoint
        self._resource = boto3.resource("dynamodb", **kwargs)
        self._tables: dict[str, Any] = {}

    def table(self, name: str):
        if name not in self._tables:
            self._tables[name] = self._resource.Table(name)
        return self._tables[name]

    # ── CRUD helpers ─────────────────────────────────────────────────────

    def put_item(self, table_name: str, item: dict) -> None:
        self.table(table_name).put_item(Item=item)
        logger.debug("put_item table=%s id=%s", table_name, next(iter(item.values())))

    def get_item(self, table_name: str, key: dict) -> dict | None:
        resp = self.table(table_name).get_item(Key=key)
        return resp.get("Item")

    def query(
        self,
        table_name: str,
        index_name: str | None = None,
        key_condition: Any = None,
        **kwargs,
    ) -> list[dict]:
        params: dict[str, Any] = {"KeyConditionExpression": key_condition, **kwargs}
        if index_name:
            params["IndexName"] = index_name
        resp = self.table(table_name).query(**params)
        return resp.get("Items", [])

    def update_item(self, table_name: str, key: dict, update_expr: str, expr_values: dict, expr_names: dict | None = None) -> None:
        params: dict[str, Any] = {
            "Key": key,
            "UpdateExpression": update_expr,
            "ExpressionAttributeValues": expr_values,
        }
        if expr_names:
            params["ExpressionAttributeNames"] = expr_names
        self.table(table_name).update_item(**params)

    def scan(self, table_name: str, filter_expression: Any = None, **kwargs) -> list[dict]:
        params = {**kwargs}
        if filter_expression is not None:
            params["FilterExpression"] = filter_expression
        resp = self.table(table_name).scan(**params)
        return resp.get("Items", [])
