import pytest
from fastapi import status
from httpx import AsyncClient
from pydantic import EmailStr
from pymongo.asynchronous.database import AsyncDatabase

from models.user import User
from utils.password import verify_password

_test_case = [
    "email,password",
    [
        ("user1@example.com", "P@ssw0rd123!"),
        ("user2@example.com", "StrongPass456!"),
    ],
]


@pytest.mark.parametrize(*_test_case)
async def test_create_user(client: AsyncClient, db_test: AsyncDatabase, email: EmailStr, password: str) -> None:
    res = await client.post(
        "/users",
        json={
            "email": email,
            "password": password,
        },
    )

    assert res.status_code == status.HTTP_201_CREATED

    res_data = res.json()
    assert res_data["email"] == email

    user = await db_test[User.__collection_name__].find_one({"email": email})

    assert user is not None
    assert user["email"] == email
    assert str(user["_id"]) == res_data["id"]

    assert verify_password(plain_password=password, hashed_password=user["password"])
