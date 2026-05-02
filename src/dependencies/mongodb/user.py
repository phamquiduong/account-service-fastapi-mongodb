from typing import Annotated

from fastapi import Depends

import settings
from dependencies.mongodb._client import MongoClientDep
from models._base import BaseMongoManager
from models.user import User


def _get_user_mongo_manager(client: MongoClientDep) -> BaseMongoManager[User]:
    return BaseMongoManager(client=client, db_name=settings.DB_NAME, model=User)


UserMongoManagerDep = Annotated[BaseMongoManager[User], Depends(_get_user_mongo_manager)]
