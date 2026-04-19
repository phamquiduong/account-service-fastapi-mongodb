from typing import Annotated

from fastapi import Depends

import settings
from models.base import BaseMongoManager
from models.user import User


def _get_user_repository():
    yield BaseMongoManager.from_uri(uri=settings.DB_URI, db_name=settings.DB_NAME, model=User)


UserRepositoryDep = Annotated[BaseMongoManager[User], Depends(_get_user_repository)]
