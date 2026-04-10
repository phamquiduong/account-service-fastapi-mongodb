from fastapi import APIRouter

from dependencies.user import UserMongoManagerDep
from models.user import User

user_router = APIRouter(prefix="/users")


@user_router.get("")
async def get_all_users(user_mongo_manager: UserMongoManagerDep) -> list[User]:
    return await user_mongo_manager.list()
