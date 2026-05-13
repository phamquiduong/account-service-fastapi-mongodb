import uuid

import pytest
from fastapi import status
from httpx import AsyncClient
from pydantic import EmailStr
from pymongo.asynchronous.database import AsyncDatabase

from models.user import User
from utils.password import get_password_hash
from utils.token import decode_auth_token

_test_case = [
    "_id,email,password",
    [
        (uuid.uuid7(), "user1@example.com", "P@ssw0rd123!"),
    ],
]


@pytest.mark.parametrize(*_test_case)
async def test_login_user(
    client: AsyncClient, db_test: AsyncDatabase, _id: uuid.UUID, email: EmailStr, password: str
) -> None:
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

    assert res.status_code == status.HTTP_200_OK

    res_data = res.json()

    access_token = res_data.get("access", "")
    access_payload = decode_auth_token(access_token)
    assert access_payload.user_id == _id
    assert access_payload.token_type == "access"

    refresh = res_data.get("refresh", "")
    refresh_payload = decode_auth_token(refresh)
    assert refresh_payload.user_id == _id
    assert refresh_payload.token_type == "refresh"
