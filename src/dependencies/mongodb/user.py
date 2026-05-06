from typing import Annotated

from fastapi import Depends

from dependencies.mongodb._connection import MongoDatabaseDep
from models._base import BaseMongoManager
from models.user import User


def _get_user_mongo_manager(db: MongoDatabaseDep) -> BaseMongoManager[User]:
    return BaseMongoManager(db=db, model=User)


UserMongoManagerDep = Annotated[BaseMongoManager[User], Depends(_get_user_mongo_manager)]
