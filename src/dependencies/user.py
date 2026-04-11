from typing import Annotated

from fastapi import Depends

import settings
from models.base import BaseMongoManager
from models.user import User


async def _get_user_manager():
    yield BaseMongoManager(uri=settings.DB_URI, db_name=settings.DB_NAME, collection_name="users", model=User)


UserMongoManagerDep = Annotated[BaseMongoManager[User], Depends(_get_user_manager)]
