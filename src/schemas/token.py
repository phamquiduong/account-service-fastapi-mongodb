import uuid
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid7

from pydantic import BaseModel, Field

import settings
from models.user import User


class FastAPIToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenData(BaseModel):
    user_id: uuid.UUID
    token_version: uuid.UUID
    token_type: TokenType
    exp: datetime
    jti: UUID = Field(default_factory=uuid7)
    iat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def access(cls, user: User, token_version: uuid.UUID):
        now = datetime.now(timezone.utc)
        return cls(
            user_id=user.id,
            token_version=token_version,
            token_type=TokenType.ACCESS,
            exp=now + settings.ACCESS_TOKEN_EXPIRE,
        )

    @classmethod
    def refresh(cls, user: User, token_version: uuid.UUID):
        now = datetime.now(timezone.utc)
        return cls(
            user_id=user.id,
            token_version=token_version,
            token_type=TokenType.REFRESH,
            exp=now + settings.REFRESH_TOKEN_EXPIRE,
        )


class TokenResponse(BaseModel):
    access: str = Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIn0."
            "aNdCny8GHuapLKUUsigSUh5m8hc84sbOH5IsnA2h8w4"
        ]
    )
    refresh: str = Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ0b2tlbl90eXBlIjoicmVmcmVzaCJ9."
            "kxE_j_9e0YgSIQ5Gh-UqR8_4N4vuFtLjKtvbs1st4k4"
        ]
    )
