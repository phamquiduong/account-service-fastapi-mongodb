from fastapi import APIRouter, Body, HTTPException, status
from pydantic import EmailStr

from dependencies.user import UserMongoManagerDep
from models.user import User
from utils.password import get_password_hash

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("")
async def get_all_users(user_mongo_manager: UserMongoManagerDep) -> list[User]:
    return await user_mongo_manager.list()


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user_mongo_manager: UserMongoManagerDep, email: EmailStr = Body(), password: str = Body()
) -> User:
    if await user_mongo_manager.get({"email": email}) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user = User(email=email, password=get_password_hash(password))
    await user_mongo_manager.create(user)
    return user
