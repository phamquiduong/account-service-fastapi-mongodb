import logging

from fastapi import APIRouter, HTTPException, status

from dependencies.services.user import UserServiceDep
from models.user import User
from schemas.list import ListQueryDep
from schemas.user import UserRegisterRequest

_logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("")
async def get_all_users(user_service: UserServiceDep, list_query: ListQueryDep) -> list[User]:
    return await user_service.list(skip=list_query.skip, limit=list_query.limit)


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def register_new_user(user_service: UserServiceDep, request: UserRegisterRequest) -> User:
    certificate_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Register failed")

    if await user_service.get_by_email(email=request.email) is not None:
        _logger.warning("user with email [%s] already exist", request.email)
        raise certificate_error

    return await user_service.create(email=request.email, password=request.password)
