from typing import Annotated

from fastapi import Depends

import settings
from models.base import BaseMongoManager
from models.token_version import TokenVersion
from models.user import User
from services.user import UserService


def _get_user_repository():
    yield BaseMongoManager.from_uri(uri=settings.DB_URI, db_name=settings.DB_NAME, model=User)


_UserRepositoryDep = Annotated[BaseMongoManager[User], Depends(_get_user_repository)]


def _get_token_version_repository():
    yield BaseMongoManager.from_uri(uri=settings.DB_URI, db_name=settings.DB_NAME, model=TokenVersion)


_TokenVersionRepositoryDep = Annotated[BaseMongoManager[TokenVersion], Depends(_get_token_version_repository)]


def _get_user_service(
    user_repository: _UserRepositoryDep,
    token_version_repository: _TokenVersionRepositoryDep,
) -> UserService:
    return UserService(user_repository, token_version_repository)


UserServiceDep = Annotated[UserService, Depends(_get_user_service)]
