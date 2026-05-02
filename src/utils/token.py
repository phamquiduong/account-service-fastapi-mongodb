from json import JSONEncoder
from typing import Any, override
from uuid import UUID

import jwt

import settings
from schemas.token import TokenData


class _Encoder(JSONEncoder):
    @override
    def default(self, o: Any) -> Any:
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)


def _encode_jwt_token(data: dict, secret_key: str, algorithm: str) -> str:
    to_encode = data.copy()
    encoded_jwt = jwt.encode(payload=to_encode, key=secret_key, algorithm=algorithm, json_encoder=_Encoder)
    return encoded_jwt


def _decode_jwt(token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
    return jwt.decode(jwt=token, key=secret_key, algorithms=[algorithm])


def create_auth_token(token_data: TokenData) -> str:
    return _encode_jwt_token(data=token_data.model_dump(), secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_auth_token(token: str) -> TokenData:
    payload = _decode_jwt(token=token, secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return TokenData.model_validate(payload)
