from typing import Annotated

from fastapi import Depends

from models.base import BaseMongoManager
from models.user import User
from settings import MONGODB_URI


async def get_user_manager():
    yield BaseMongoManager(uri=MONGODB_URI, db_name="account-service-testing", collection_name="users", model=User)


UserMongoManagerDep = Annotated[BaseMongoManager[User], Depends(get_user_manager)]
