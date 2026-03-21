from __future__ import annotations

import logging
from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.config import Settings, get_settings
from app.infrastructure.database import DynamoDBClient
from app.infrastructure.llm.factory import create_llm_provider
from app.infrastructure.repositories.file_repository import FileRepository
from app.infrastructure.repositories.transaction_repository import TransactionRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.storage import S3Client
from app.services.auth_service import AuthService
from app.services.categorization_service import CategorizationService
from app.services.dashboard_service import DashboardService
from app.services.file_upload_service import FileUploadService
from app.services.parser_service import ParserService
from app.services.transaction_service import TransactionService

logger = logging.getLogger(__name__)

# ── Singleton-ish infrastructure (created once per cold start) ───────────────

_db: DynamoDBClient | None = None
_s3: S3Client | None = None


def get_db() -> DynamoDBClient:
    global _db
    if _db is None:
        _db = DynamoDBClient()
    return _db


def get_s3() -> S3Client:
    global _s3
    if _s3 is None:
        _s3 = S3Client()
    return _s3


# ── Repositories ─────────────────────────────────────────────────────────────

def get_user_repo(db: DynamoDBClient = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_txn_repo(db: DynamoDBClient = Depends(get_db)) -> TransactionRepository:
    return TransactionRepository(db)


def get_file_repo(db: DynamoDBClient = Depends(get_db)) -> FileRepository:
    return FileRepository(db)


# ── Services ─────────────────────────────────────────────────────────────────

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    return AuthService(user_repo, settings)


def get_categorization_service(
    settings: Settings = Depends(get_settings),
) -> CategorizationService:
    try:
        llm = create_llm_provider(settings)
    except Exception:
        logger.warning("LLM provider unavailable, using rule-based categorization")
        llm = None
    return CategorizationService(llm)


def get_file_upload_service(
    s3: S3Client = Depends(get_s3),
    file_repo: FileRepository = Depends(get_file_repo),
    settings: Settings = Depends(get_settings),
) -> FileUploadService:
    return FileUploadService(s3, file_repo, settings)


def get_transaction_service(
    txn_repo: TransactionRepository = Depends(get_txn_repo),
    file_repo: FileRepository = Depends(get_file_repo),
    s3: S3Client = Depends(get_s3),
    categorizer: CategorizationService = Depends(get_categorization_service),
) -> TransactionService:
    return TransactionService(txn_repo, file_repo, s3, ParserService(), categorizer)


def get_dashboard_service(
    txn_repo: TransactionRepository = Depends(get_txn_repo),
) -> DashboardService:
    return DashboardService(txn_repo)


# ── Auth dependency ──────────────────────────────────────────────────────────

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> str:
    """Extract and verify JWT from Authorization header. Returns user_id."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        return auth_service.verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
