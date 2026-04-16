import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from dependencies.services.user import UserServiceDep
from models.user import User
from schemas.token import TokenData, TokenType
from utils.token import decode_auth_token

_logger = logging.getLogger(__name__)

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def _get_token_data(token: Annotated[str, Depends(_oauth2_scheme)]) -> TokenData:
    try:
        token_data = decode_auth_token(token)
    except InvalidTokenError as exc:
        _logger.warning("Authenticate failed. Detail: %s", exc)

    if token_data.token_type != TokenType.ACCESS:
        _logger.warning("Authenticate failed. Token type [%s] invalid", token_data.token_type)
        raise _credentials_exception

    return token_data


TokenDataDep = Annotated[TokenData, Depends(_get_token_data)]


async def _get_auth_user(user_service: UserServiceDep, token_data: TokenDataDep) -> User:
    user = await user_service.get_by_id(token_data.user_id)

    if user is None:
        _logger.warning("User with id [%s] does not exist", token_data.user_id)
        raise _credentials_exception

    return user


AuthUserDep = Annotated[User, Depends(_get_auth_user)]
