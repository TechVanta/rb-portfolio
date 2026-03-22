from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_dashboard_service
from app.domain.models import DashboardResponse
from app.services.dashboard_service import DashboardService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    user_id: str = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    return dashboard_service.get_dashboard(user_id)
