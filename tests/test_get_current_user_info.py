import uuid

from fastapi import status
from httpx import AsyncClient
from pydantic import BaseModel, EmailStr


class _AuthData(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    access: str
    refresh: str


async def test_create_user(client: AsyncClient, auth_data: _AuthData) -> None:
    res = await client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {auth_data.access}",
        },
    )

    assert res.status_code == status.HTTP_200_OK

    res_data = res.json()

    assert res_data["id"] == str(auth_data.user_id)
    assert res_data["email"] == auth_data.email
