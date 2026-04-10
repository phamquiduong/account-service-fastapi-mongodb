from pydantic import EmailStr

from models.base import MongoModel


class User(MongoModel):
    email: EmailStr
    password: str
