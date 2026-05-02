import uuid

import pytest
from fastapi import status
from httpx import AsyncClient
from pydantic import EmailStr
from pymongo.asynchronous.database import AsyncDatabase

from models.user import User
from utils.password import get_password_hash

_test_case = [
    "users",
    [
        [
            (uuid.uuid7(), "user1@example.com", "P@ssw0rd123!"),
            (uuid.uuid7(), "user2@example.com", "P@ssw0rd123!"),
            (uuid.uuid7(), "user3@example.com", "P@ssw0rd123!"),
            (uuid.uuid7(), "user4@example.com", "P@ssw0rd123!"),
            (uuid.uuid7(), "user5@example.com", "P@ssw0rd123!"),
        ],
    ],
]


@pytest.mark.parametrize(*_test_case)
async def test_create_user(
    client: AsyncClient, db_test: AsyncDatabase, users: list[tuple[uuid.UUID, EmailStr, str]]
) -> None:
    for _id, email, password in users:
        await db_test[User.__collection_name__].insert_one(
            {
                "_id": _id,
                "email": email,
                "password": get_password_hash(password),
            }
        )

    res = await client.get(
        "/users",
        params={
            "skip": 0,
            "limit": 10,
        },
    )

    assert res.status_code == status.HTTP_200_OK

    res_data = res.json()

    assert len(res_data) == len(users)

    for _id, email, password in users:
        user = next((u for u in res_data if u["id"] == str(_id)), None)
        assert user is not None
        assert user["email"] == email
