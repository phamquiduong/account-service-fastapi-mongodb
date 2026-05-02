import os
import sys

import pytest
from httpx import ASGITransport, AsyncClient
from pymongo import AsyncMongoClient

sys.path.append(os.path.abspath("src"))

os.environ["SECRET_KEY"] = "test_secret"
os.environ["DB_NAME"] = "account-service-testing"
os.environ["DB_URI"] = "mongodb://admin:IctJBI4rnILrbMFB@localhost:27017"


@pytest.fixture
async def db_client():
    client = AsyncMongoClient(os.environ["DB_URI"], uuidRepresentation="standard")
    yield client
    await client.drop_database(os.environ["DB_NAME"])
    await client.close()


@pytest.fixture
async def db_test(db_client):
    return db_client[os.environ["DB_NAME"]]


@pytest.fixture
async def client(db_client):
    from dependencies.user import _get_user_repository
    from main import app
    from models.base import BaseMongoManager
    from models.user import User

    async def override_get_user_repository():
        yield BaseMongoManager(db_client, db_name=os.environ["DB_NAME"], model=User)

    app.dependency_overrides[_get_user_repository] = override_get_user_repository

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides = {}
