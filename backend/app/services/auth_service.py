from __future__ import annotations

import logging
from datetime import datetime, timedelta

import bcrypt
import jwt

from app.config import Settings
from app.domain.exceptions import AuthenticationError
from app.domain.models import TokenResponse, UserCreate, UserInDB, UserResponse
from app.infrastructure.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repo: UserRepository, settings: Settings):
        self._repo = user_repo
        self._settings = settings

    def signup(self, data: UserCreate) -> UserResponse:
        existing = self._repo.get_by_email(data.email)
        if existing:
            raise AuthenticationError("Email already registered")

        password_hash = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = UserInDB(email=data.email, password_hash=password_hash)
        self._repo.create(user)
        logger.info("User created: %s", user.user_id)
        return UserResponse(user_id=user.user_id, email=user.email)

    def login(self, email: str, password: str) -> TokenResponse:
        user = self._repo.get_by_email(email)
        if not user:
            raise AuthenticationError("Invalid email or password")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise AuthenticationError("Invalid email or password")

        token = self._create_token(user.user_id)
        logger.info("User logged in: %s", user.user_id)
        return TokenResponse(access_token=token)

    def verify_token(self, token: str) -> str:
        """Returns user_id if token is valid."""
        try:
            payload = jwt.decode(
                token,
                self._settings.jwt_secret,
                algorithms=[self._settings.jwt_algorithm],
            )
            user_id: str = payload["sub"]
            return user_id
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

    def _create_token(self, user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self._settings.jwt_expiration_minutes)
        payload = {"sub": user_id, "exp": expire}
        return jwt.encode(payload, self._settings.jwt_secret, algorithm=self._settings.jwt_algorithm)
