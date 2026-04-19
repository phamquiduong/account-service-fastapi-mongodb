import pytest
from fastapi import status

_test_case = [
    "email,password",
    [
        ("user1@example.com", "P@ssw0rd123!"),
        ("user2@example.com", "StrongPass456!"),
    ],
]


@pytest.mark.anyio
@pytest.mark.parametrize(*_test_case)
async def test_create_user(client, db_test, email, password):
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

    user = await db_test["users"].find_one({"email": email})

    assert user is not None
    assert user["email"] == email
    assert str(user["_id"]) == res_data["id"]
