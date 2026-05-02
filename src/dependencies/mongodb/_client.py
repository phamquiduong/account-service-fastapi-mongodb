from typing import Annotated

from fastapi import Depends
from pymongo import AsyncMongoClient

import settings


def get_mongo_client():
    return AsyncMongoClient(settings.DB_URI, uuidRepresentation="standard")


MongoClientDep = Annotated[AsyncMongoClient, Depends(get_mongo_client)]
