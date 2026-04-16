from typing import Annotated

from fastapi import Depends

from dependencies.repositories.user import UserRepositoryDep
from services.user import UserService


def _get_user_service(user_repository: UserRepositoryDep):
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(_get_user_service)]
