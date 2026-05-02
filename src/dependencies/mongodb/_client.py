from typing import Annotated

from fastapi import Depends
from pymongo import AsyncMongoClient

import settings


def _get_mongo_client() -> AsyncMongoClient:
    return AsyncMongoClient(settings.DB_URI, uuidRepresentation="standard")


MongoClientDep = Annotated[AsyncMongoClient, Depends(_get_mongo_client)]
