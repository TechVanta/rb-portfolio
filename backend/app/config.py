from __future__ import annotations

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────────────
    app_name: str = "FinTrack"
    debug: bool = False
    log_level: str = "INFO"
    allowed_origins: str = "*"  # comma-separated for production

    # ── Auth ─────────────────────────────────────────────────────────────
    jwt_secret: str = "CHANGE-ME-IN-PRODUCTION"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24  # 24 hours

    # ── AWS ──────────────────────────────────────────────────────────────
    aws_region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    # ── DynamoDB ─────────────────────────────────────────────────────────
    dynamodb_endpoint: str | None = None  # For local dev
    users_table: str = "fintrack-users"
    transactions_table: str = "fintrack-transactions"
    files_table: str = "fintrack-files"

    # ── S3 ───────────────────────────────────────────────────────────────
    s3_endpoint: str | None = None  # For local dev
    s3_bucket: str = "fintrack-uploads"

    # ── LLM ──────────────────────────────────────────────────────────────
    llm_provider: str = "openai"  # openai | grok
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    grok_api_key: str | None = None
    grok_model: str = "grok-3-mini"
    grok_base_url: str = "https://api.x.ai/v1"

    # ── Upload limits ────────────────────────────────────────────────────
    max_upload_size_mb: int = 10

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
