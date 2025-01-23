from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.repositories.sqlalchemy.uow import UnitOfWork
from app.core.settings import settings
from app.core.utils import JWTHandler
from app.habit_tracker.service.habits import HabitsService


def get_service(srv_class):
    """Init service."""

    def dep(request: fastapi.Request):
        """Init depends."""
        uow = UnitOfWork(request.app.state.pg_async_session_maker)
        return srv_class(uow)

    return dep


LeadsDEP = Annotated[HabitsService, Depends(get_service(HabitsService))]

http_bearer = HTTPBearer(auto_error=False)


def get_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
) -> dict:
    """
    Зависимость для извлечения токена.
    Токен больше не отображается в Swagger UI.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail="Authorization token is missing",
        )
    jwt_handler = JWTHandler(secret_key=settings.secret_key)
    payload = jwt_handler.decode_token(credentials.credentials.encode())
    return payload


def is_valid_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
) -> bool:
    """
    Зависимость для извлечения токена.
    Токен больше не отображается в Swagger UI.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail="Authorization token is missing",
        )
    jwt_handler = JWTHandler(secret_key=settings.secret_key)
    return jwt_handler.is_token_valid(credentials)
