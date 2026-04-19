from pydantic import EmailStr, Field

from models.base import MongoModel


class User(MongoModel):
    __collection_name__ = "users"

    email: EmailStr
    password: str = Field(exclude=True)
