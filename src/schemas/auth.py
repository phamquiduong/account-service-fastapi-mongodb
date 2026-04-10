from pydantic import BaseModel, EmailStr

from fields.password import PasswordStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
