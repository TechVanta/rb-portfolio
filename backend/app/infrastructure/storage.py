from __future__ import annotations

import logging
from typing import Any

import boto3

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


class S3Client:
    """Thin wrapper around boto3 S3 client."""

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        kwargs: dict[str, Any] = {"region_name": self._settings.aws_region}
        if self._settings.aws_access_key_id:
            kwargs["aws_access_key_id"] = self._settings.aws_access_key_id
            kwargs["aws_secret_access_key"] = self._settings.aws_secret_access_key
        if self._settings.s3_endpoint:
            kwargs["endpoint_url"] = self._settings.s3_endpoint
        self._client = boto3.client("s3", **kwargs)
        self._bucket = self._settings.s3_bucket

    def upload_bytes(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        self._client.put_object(
            Bucket=self._bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
        )
        s3_path = f"s3://{self._bucket}/{key}"
        logger.info("Uploaded %s (%d bytes)", s3_path, len(data))
        return s3_path

    def download_bytes(self, key: str) -> bytes:
        resp = self._client.get_object(Bucket=self._bucket, Key=key)
        return resp["Body"].read()

    def generate_presigned_url(self, key: str, expiration: int = 3600) -> str:
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=expiration,
        )
