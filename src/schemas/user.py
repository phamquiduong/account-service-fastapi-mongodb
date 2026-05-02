from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator

from fields.password import PasswordStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class AuthUserChangePasswordRequest(BaseModel):
    current_password: PasswordStr
    new_password: PasswordStr

    @field_validator("new_password")
    def validate_new_password(cls, v, info: ValidationInfo):
        current_password = info.data.get("current_password")

        if current_password and v == current_password:
            raise ValueError("New password must be different from current password")

        return v
