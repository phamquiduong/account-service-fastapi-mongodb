from fastapi import APIRouter, HTTPException, status

from dependencies.user import UserMongoManagerDep
from models.user import User
from schemas.user import UserRegisterRequest
from utils.password import get_password_hash

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("")
async def get_all_users(user_mongo_manager: UserMongoManagerDep) -> list[User]:
    return await user_mongo_manager.list()


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def register_new_user(user_mongo_manager: UserMongoManagerDep, request: UserRegisterRequest) -> User:
    if await user_mongo_manager.get({"email": request.email}) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user = User(email=request.email, password=get_password_hash(request.password))
    await user_mongo_manager.create(user)
    return user
