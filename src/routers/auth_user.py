import logging

from fastapi import APIRouter

from dependencies.auth import AuthUserDep
from models.user import User

_logger = logging.getLogger(__name__)

auth_user_router = APIRouter(prefix="/users/me", tags=["Authenticated user"])


@auth_user_router.get("")
async def get_current_user_info(auth_user: AuthUserDep) -> User:
    return auth_user
