from __future__ import annotations

import logging
import uuid

from app.config import Settings
from app.domain.enums import FileProcessingStatus, FileType
from app.domain.exceptions import ValidationError
from app.domain.models import FileRecord, FileUploadResponse
from app.infrastructure.repositories.file_repository import FileRepository
from app.infrastructure.storage import S3Client

logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {
    "application/pdf": FileType.PDF,
    "text/csv": FileType.CSV,
    "application/vnd.ms-excel": FileType.CSV,
}

MAX_FILENAME_LENGTH = 255


class FileUploadService:
    def __init__(self, s3: S3Client, file_repo: FileRepository, settings: Settings):
        self._s3 = s3
        self._repo = file_repo
        self._settings = settings

    async def upload(
        self,
        user_id: str,
        filename: str,
        content_type: str,
        file_data: bytes,
    ) -> FileUploadResponse:
        # Validate file type
        file_type = ALLOWED_CONTENT_TYPES.get(content_type)
        if not file_type:
            raise ValidationError(f"Unsupported file type: {content_type}. Allowed: PDF, CSV")

        # Validate size
        max_bytes = self._settings.max_upload_size_mb * 1024 * 1024
        if len(file_data) > max_bytes:
            raise ValidationError(f"File too large. Max: {self._settings.max_upload_size_mb}MB")

        if len(filename) > MAX_FILENAME_LENGTH:
            raise ValidationError("Filename too long")

        # Generate unique S3 key
        file_id = str(uuid.uuid4())
        safe_ext = "pdf" if file_type == FileType.PDF else "csv"
        s3_key = f"uploads/{user_id}/{file_id}.{safe_ext}"

        # Upload to S3
        s3_path = self._s3.upload_bytes(s3_key, file_data, content_type)

        # Create DB record
        record = FileRecord(
            file_id=file_id,
            user_id=user_id,
            filename=filename,
            file_type=file_type,
            s3_path=s3_path,
            status=FileProcessingStatus.PENDING,
        )
        self._repo.create(record)

        logger.info("File uploaded: %s by user %s", file_id, user_id)
        return FileUploadResponse(
            file_id=file_id,
            filename=filename,
            status=FileProcessingStatus.PENDING,
        )
