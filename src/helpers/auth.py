import logging

from fastapi import HTTPException, status
from pydantic import EmailStr

from dependencies.services.user import UserServiceDep
from models.user import User
from utils.password import verify_password

_logger = logging.getLogger(__name__)

_certificate_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login failed")


async def authenticate_user(user_service: UserServiceDep, email: EmailStr, password: str) -> User:
    user = await user_service.get_by_email(email=email)

    if user is None:
        _logger.warning("user with email [%s] does not exist", email)
        raise _certificate_error

    if verify_password(plain_password=password, hashed_password=user.password) is False:
        _logger.warning("user with email [%s] wrong password", email)
        raise _certificate_error

    return user
