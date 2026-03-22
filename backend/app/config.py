from __future__ import annotations

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────────────
    app_name: str = "FinTrack"
    debug: bool = False
    log_level: str = "INFO"
    allowed_origins: str = "*"

    # ── Auth (hardcoded) ─────────────────────────────────────────────────
    jwt_secret: str = "f1ntr4ck-s3cr3t-k3y-2026-prod-x9m2v"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24  # 24 hours

    # ── AWS (hardcoded) ──────────────────────────────────────────────────
    aws_region: str = "us-east-1"

    # ── DynamoDB (hardcoded) ─────────────────────────────────────────────
    dynamodb_endpoint: str | None = None  # For local dev
    users_table: str = "fintrack-users-production"
    transactions_table: str = "fintrack-transactions-production"
    files_table: str = "fintrack-files-production"

    # ── S3 (hardcoded) ───────────────────────────────────────────────────
    s3_endpoint: str | None = None  # For local dev
    s3_bucket: str = "fintrack-uploads-production"

    # ── LLM (from env / GitHub Secrets) ──────────────────────────────────
    llm_provider: str = "groq"  # openai | grok | groq
    llm_api_key: str = ""  # single key for whichever provider is active
    openai_model: str = "gpt-4o-mini"
    grok_model: str = "grok-3-mini"
    grok_base_url: str = "https://api.x.ai/v1"
    groq_model: str = "llama-3.3-70b-versatile"

    # ── Upload limits ────────────────────────────────────────────────────
    max_upload_size_mb: int = 10

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
