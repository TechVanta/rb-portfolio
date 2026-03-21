from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_transaction_service
from app.domain.models import TransactionListResponse
from app.services.transaction_service import TransactionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionListResponse)
def list_transactions(
    user_id: str = Depends(get_current_user),
    txn_service: TransactionService = Depends(get_transaction_service),
):
    return txn_service.get_transactions(user_id)
