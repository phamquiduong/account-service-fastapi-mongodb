from pydantic import EmailStr, Field

from models.base import MongoModel


class User(MongoModel):
    email: EmailStr
    password: str = Field(exclude=True)
