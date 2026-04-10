from pydantic import BaseModel, EmailStr

from fields.password import PasswordStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
