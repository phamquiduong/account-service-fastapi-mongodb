import os
import sys

import mongomock_motor
import pytest
from httpx import ASGITransport, AsyncClient

sys.path.append(os.path.abspath("src"))

os.environ["SECRET_KEY"] = "test_secret"
os.environ["DB_NAME"] = "account-service-testing"
os.environ["DB_URI"] = "mongodb://test:test@localhost:27017"


@pytest.fixture
async def db_client():
    return mongomock_motor.AsyncMongoMockClient()


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
