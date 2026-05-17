import os
import sys
import uuid
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel, EmailStr
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

sys.path.append(os.path.abspath("src"))

os.environ.setdefault("SECRET_KEY", "B50HiHr6w1JTR0P2zcWOcGthEGJOzqzxuym2S7FNhrE=")
os.environ.setdefault("DB_NAME", f"test_{uuid.uuid4()}")
os.environ.setdefault("DB_URI", "mongodb://admin:IctJBI4rnILrbMFB@localhost:27017")


class _AuthData(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    access: str
    refresh: str


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
async def client(db_test: AsyncDatabase) -> AsyncGenerator[AsyncClient]:
    from dependencies.mongodb._connection import _get_mongo_database
    from main import app

    async def override_get_mongo_database():
        return db_test

    app.dependency_overrides[_get_mongo_database] = override_get_mongo_database

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides = {}


@pytest.fixture
async def auth_data(client: AsyncClient, db_test: AsyncDatabase) -> _AuthData:
    from models.user import User
    from utils.password import get_password_hash

    _id = uuid.uuid7()
    email = "test@example.com"
    password = "P@ssw0rd123!"

    await db_test[User.__collection_name__].insert_one(
        {
            "_id": _id,
            "email": email,
            "password": get_password_hash(password),
        }
    )

    res = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    data = res.json()

    return _AuthData(
        user_id=_id,
        email=email,
        access=data["access"],
        refresh=data["refresh"],
    )
