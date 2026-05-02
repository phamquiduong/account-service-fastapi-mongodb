from typing import Annotated

from fastapi import Depends

from dependencies.mongodb.user import UserMongoManagerDep
from services.user import UserService


def _get_user_service(user_mongo_manager: UserMongoManagerDep) -> UserService:
    return UserService(user_mongo_manager=user_mongo_manager)


UserServiceDep = Annotated[UserService, Depends(_get_user_service)]
