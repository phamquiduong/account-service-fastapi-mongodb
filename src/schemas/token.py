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
    user_id: str
    token_type: TokenType
    exp: datetime
    jti: UUID = Field(default_factory=uuid7)
    iat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def access(cls, user: User):
        now = datetime.now(timezone.utc)
        return cls(user_id=user.id, token_type=TokenType.ACCESS, exp=now + settings.ACCESS_TOKEN_EXPIRE)

    @classmethod
    def refresh(cls, user: User):
        now = datetime.now(timezone.utc)
        return cls(user_id=user.id, token_type=TokenType.REFRESH, exp=now + settings.REFRESH_TOKEN_EXPIRE)


class TokenResponse(BaseModel):
    access: str = Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ1c2VyX2lkIjoiNjlkOGI0ZGY2OGI0ZGM5NTU3YWRkNTUyIiwidG9rZW5fdHlwZSI6ImFjY2VzcyJ9."
            "kZWhX7TzrYKBdpyNOKemFlATZAE-dBW54zrrjQdB6YQ"
        ]
    )
    refresh: str = Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ1c2VyX2lkIjoiNjlkOGI0ZGY2OGI0ZGM5NTU3YWRkNTUyIiwidG9rZW5fdHlwZSI6InJlZnJlc2gifQ."
            "jeoVYVioo538apWKyGl0UlE6lOrQugKTNusQlOLt_OU"
        ]
    )
