from __future__ import annotations

import logging
from decimal import Decimal

from app.domain.enums import FileProcessingStatus, FileType
from app.domain.exceptions import FileProcessingError, NotFoundError
from app.domain.models import (
    FileRecord,
    FileStatusResponse,
    Transaction,
    TransactionListResponse,
    TransactionResponse,
)
from app.infrastructure.repositories.file_repository import FileRepository
from app.infrastructure.repositories.transaction_repository import TransactionRepository
from app.infrastructure.storage import S3Client
from app.services.categorization_service import CategorizationService
from app.services.parser_service import ParserService

logger = logging.getLogger(__name__)


class TransactionService:
    """Orchestrates the full file-processing pipeline: parse → categorize → persist."""

    def __init__(
        self,
        txn_repo: TransactionRepository,
        file_repo: FileRepository,
        s3: S3Client,
        parser: ParserService,
        categorizer: CategorizationService,
    ):
        self._txn_repo = txn_repo
        self._file_repo = file_repo
        self._s3 = s3
        self._parser = parser
        self._categorizer = categorizer

    async def process_file(self, file_id: str, user_id: str) -> FileStatusResponse:
        """Full pipeline: download → parse → categorize → persist."""
        record = self._file_repo.get_by_id(file_id)
        if not record:
            raise NotFoundError("File", file_id)
        if record.user_id != user_id:
            raise NotFoundError("File", file_id)

        # Mark processing
        self._file_repo.update_status(file_id, FileProcessingStatus.PROCESSING.value)

        try:
            # 1. Download from S3
            s3_key = record.s3_path.replace(f"s3://{self._s3._bucket}/", "")
            file_data = self._s3.download_bytes(s3_key)

            # 2. Parse
            raw_transactions = self._parser.parse(file_data, FileType(record.file_type))

            # 3. Categorize
            items = [(t.description, t.amount) for t in raw_transactions]
            categories = await self._categorizer.categorize_batch(items)

            # 4. Persist
            transactions: list[Transaction] = []
            for raw, cat_result in zip(raw_transactions, categories):
                txn = Transaction(
                    user_id=user_id,
                    file_id=file_id,
                    date=raw.date,
                    description=raw.description,
                    amount=Decimal(str(raw.amount)),
                    category=cat_result.category,
                )
                transactions.append(txn)

            self._txn_repo.create_batch(transactions)

            # 5. Update file status
            self._file_repo.update_status(
                file_id,
                FileProcessingStatus.COMPLETED.value,
                transaction_count=len(transactions),
            )

            logger.info("Processed file %s: %d transactions", file_id, len(transactions))
            return FileStatusResponse(
                file_id=file_id,
                filename=record.filename,
                status=FileProcessingStatus.COMPLETED,
                transaction_count=len(transactions),
                upload_date=record.upload_date,
            )

        except FileProcessingError as exc:
            self._file_repo.update_status(
                file_id, FileProcessingStatus.FAILED.value, error_message=str(exc)
            )
            raise
        except Exception as exc:
            logger.exception("Unexpected error processing file %s", file_id)
            self._file_repo.update_status(
                file_id, FileProcessingStatus.FAILED.value, error_message="Internal processing error"
            )
            raise FileProcessingError(f"Failed to process file: {exc}")

    def get_transactions(self, user_id: str) -> TransactionListResponse:
        transactions = self._txn_repo.get_by_user(user_id)
        items = [
            TransactionResponse(
                transaction_id=t.transaction_id,
                date=t.date,
                description=t.description,
                amount=float(t.amount),
                category=t.category.value if hasattr(t.category, "value") else str(t.category),
                file_id=t.file_id,
            )
            for t in transactions
        ]
        # Sort by date descending
        items.sort(key=lambda x: x.date, reverse=True)
        return TransactionListResponse(transactions=items, count=len(items))

    def get_file_status(self, file_id: str, user_id: str) -> FileStatusResponse:
        record = self._file_repo.get_by_id(file_id)
        if not record or record.user_id != user_id:
            raise NotFoundError("File", file_id)
        return FileStatusResponse(
            file_id=record.file_id,
            filename=record.filename,
            status=FileProcessingStatus(record.status),
            transaction_count=record.transaction_count,
            error_message=record.error_message,
            upload_date=record.upload_date,
        )
