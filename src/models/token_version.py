from pydantic import Field

from models.base import MongoModel


class TokenVersion(MongoModel):
    __collection_name__ = "token_versions"

    user_id: str
    version: int = Field(default=1)
