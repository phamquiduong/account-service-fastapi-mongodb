from typing import Annotated

from fastapi import Depends

import settings
from models.base import BaseMongoManager
from models.user import User
from services.user import UserService


def _get_user_repository():
    yield BaseMongoManager.from_uri(uri=settings.DB_URI, db_name=settings.DB_NAME, model=User)


UserRepositoryDep = Annotated[BaseMongoManager[User], Depends(_get_user_repository)]


def _get_user_service(user_repository: UserRepositoryDep):
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(_get_user_service)]
