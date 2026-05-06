from typing import Annotated

from fastapi import Depends

from dependencies.mongodb._connection import MongoDatabaseDep
from models._base import BaseMongoManager
from models.token_version import TokenVersion


def _get_token_version_mongo_manager(db: MongoDatabaseDep) -> BaseMongoManager[TokenVersion]:
    return BaseMongoManager(db=db, model=TokenVersion)


TokenVersionMongoManagerDep = Annotated[BaseMongoManager[TokenVersion], Depends(_get_token_version_mongo_manager)]
