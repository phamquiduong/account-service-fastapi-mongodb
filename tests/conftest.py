import os
import sys
import uuid
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

sys.path.append(os.path.abspath("src"))

os.environ.setdefault("SECRET_KEY", "test_secret")
os.environ.setdefault("DB_NAME", f"test_{uuid.uuid4()}")
os.environ.setdefault("DB_URI", "mongodb://admin:IctJBI4rnILrbMFB@localhost:27017")


@pytest.fixture
async def db_client() -> AsyncGenerator[AsyncMongoClient]:
    client = AsyncMongoClient(os.environ["DB_URI"], uuidRepresentation="standard")
    yield client
    await client.drop_database(os.environ["DB_NAME"])
    await client.close()


@pytest.fixture
async def db_test(db_client: AsyncMongoClient) -> AsyncDatabase:
    return db_client[os.environ["DB_NAME"]]


@pytest.fixture
async def client(db_client: AsyncMongoClient) -> AsyncGenerator[AsyncClient]:
    from dependencies.mongodb._client import _get_mongo_client
    from main import app

    async def override_get_mongo_client():
        return db_client

    app.dependency_overrides[_get_mongo_client] = override_get_mongo_client

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides = {}
