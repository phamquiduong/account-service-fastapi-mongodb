from typing import Any

import jwt

import settings
from schemas.token import TokenData


def _encode_jwt_token(data: dict, secret_key: str, algorithm: str):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(payload=to_encode, key=secret_key, algorithm=algorithm)
    return encoded_jwt


def _decode_jwt(token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
    return jwt.decode(jwt=token, key=secret_key, algorithms=[algorithm])


def create_auth_token(token_data: TokenData):
    return _encode_jwt_token(data=token_data.model_dump(), secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_auth_token(token: str) -> TokenData:
    payload = _decode_jwt(token=token, secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return TokenData.model_validate(payload)
