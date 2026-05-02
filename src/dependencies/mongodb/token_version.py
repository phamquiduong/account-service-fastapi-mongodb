from typing import Annotated

from fastapi import Depends

import settings
from dependencies.mongodb._client import MongoClientDep
from models._base import BaseMongoManager
from models.token_version import TokenVersion


def _get_token_version_mongo_manager(client: MongoClientDep):
    yield BaseMongoManager(client=client, db_name=settings.DB_NAME, model=TokenVersion)


TokenVersionMongoManagerDep = Annotated[BaseMongoManager[TokenVersion], Depends(_get_token_version_mongo_manager)]
