from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.domain.enums import FileProcessingStatus, FileType, TransactionCategory


# ─── Auth / User ─────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInDB(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    password_hash: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ─── Transactions ────────────────────────────────────────────────────────────

class TransactionBase(BaseModel):
    date: str
    description: str
    amount: Decimal

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        # Accept ISO format dates
        try:
            date.fromisoformat(v)
        except ValueError as exc:
            raise ValueError("date must be in YYYY-MM-DD format") from exc
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v == 0:
            raise ValueError("amount must not be zero")
        return v


class Transaction(TransactionBase):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    category: TransactionCategory = TransactionCategory.OTHER
    file_id: Optional[str] = None


class TransactionResponse(BaseModel):
    transaction_id: str
    date: str
    description: str
    amount: float
    category: str
    file_id: Optional[str] = None


class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]
    count: int


# ─── Files ───────────────────────────────────────────────────────────────────

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    status: FileProcessingStatus


class FileRecord(BaseModel):
    file_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    filename: str
    file_type: FileType
    s3_path: str
    status: FileProcessingStatus = FileProcessingStatus.PENDING
    upload_date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    transaction_count: int = 0
    error_message: Optional[str] = None


class FileStatusResponse(BaseModel):
    file_id: str
    filename: str
    status: FileProcessingStatus
    transaction_count: int
    error_message: Optional[str] = None
    upload_date: str


# ─── Dashboard ───────────────────────────────────────────────────────────────

class CategoryBreakdown(BaseModel):
    category: str
    total: float
    count: int
    percentage: float


class MonthlySpending(BaseModel):
    month: str  # YYYY-MM
    total: float
    categories: list[CategoryBreakdown]


class DashboardResponse(BaseModel):
    total_spending: float
    transaction_count: int
    monthly_spending: list[MonthlySpending]
    category_breakdown: list[CategoryBreakdown]


# ─── LLM ─────────────────────────────────────────────────────────────────────

class CategorizationRequest(BaseModel):
    description: str
    amount: float


class CategorizationResult(BaseModel):
    category: TransactionCategory
    confidence: float = 0.0
