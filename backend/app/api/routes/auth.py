from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_auth_service
from app.domain.exceptions import AuthenticationError
from app.domain.models import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(
    data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return auth_service.signup(data)
    except AuthenticationError as exc:
        raise HTTPException(status_code=409, detail=exc.message)


@router.post("/login", response_model=TokenResponse)
def login(
    data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return auth_service.login(data.email, data.password)
    except AuthenticationError as exc:
        raise HTTPException(status_code=401, detail=exc.message)
