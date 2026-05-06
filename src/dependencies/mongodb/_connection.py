from typing import Annotated

from fastapi import Depends
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

import settings


def _get_mongo_client() -> AsyncMongoClient:
    return AsyncMongoClient(settings.DB_URI, uuidRepresentation="standard")


MongoClientDep = Annotated[AsyncMongoClient, Depends(_get_mongo_client)]


def _get_mongo_database(client: MongoClientDep) -> AsyncDatabase:
    return client[settings.DB_NAME]


MongoDatabaseDep = Annotated[AsyncDatabase, Depends(_get_mongo_database)]
