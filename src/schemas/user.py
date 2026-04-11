from pydantic import BaseModel, EmailStr, model_validator

from fields.password import PasswordStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class AuthUserChangePasswordRequest(BaseModel):
    current_password: PasswordStr
    new_password: PasswordStr

    @model_validator(mode="after")
    def check_password_not_same(self):
        if self.current_password == self.new_password:
            raise ValueError("New password must be different from current password")
        return self
