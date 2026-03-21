from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.api.deps import get_current_user, get_file_upload_service, get_transaction_service
from app.domain.exceptions import AppException
from app.domain.models import FileStatusResponse, FileUploadResponse
from app.services.file_upload_service import FileUploadService
from app.services.transaction_service import TransactionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", response_model=FileUploadResponse, status_code=201)
async def upload_file(
    file: UploadFile,
    user_id: str = Depends(get_current_user),
    upload_service: FileUploadService = Depends(get_file_upload_service),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    content_type = file.content_type or "application/octet-stream"
    data = await file.read()

    try:
        return await upload_service.upload(user_id, file.filename, content_type, data)
    except AppException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post("/{file_id}/process", response_model=FileStatusResponse)
async def process_file(
    file_id: str,
    user_id: str = Depends(get_current_user),
    txn_service: TransactionService = Depends(get_transaction_service),
):
    try:
        return await txn_service.process_file(file_id, user_id)
    except AppException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/{file_id}/status", response_model=FileStatusResponse)
def file_status(
    file_id: str,
    user_id: str = Depends(get_current_user),
    txn_service: TransactionService = Depends(get_transaction_service),
):
    try:
        return txn_service.get_file_status(file_id, user_id)
    except AppException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
