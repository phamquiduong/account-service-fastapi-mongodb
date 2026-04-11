import logging

from fastapi import APIRouter, HTTPException, status

from dependencies.auth import AuthUserDep
from dependencies.user import UserMongoManagerDep
from models.user import User
from schemas.user import UserRegisterRequest
from utils.password import get_password_hash

_logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("")
async def get_all_users(user_mongo_manager: UserMongoManagerDep) -> list[User]:
    return await user_mongo_manager.list()


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def register_new_user(user_mongo_manager: UserMongoManagerDep, request: UserRegisterRequest) -> User:
    certificate_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Register failed")

    if await user_mongo_manager.get({"email": request.email}) is not None:
        _logger.warning("user with email [%s] already exist", request.email)
        raise certificate_error

    user = User(email=request.email, password=get_password_hash(request.password))
    await user_mongo_manager.create(user)
    return user


@user_router.get("/me")
async def get_current_user_info(auth_user: AuthUserDep) -> User:
    return auth_user
