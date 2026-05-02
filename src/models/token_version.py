import uuid

from pydantic import Field

from models.base import MongoModel


class TokenVersion(MongoModel):
    __collection_name__ = "token_versions"

    user_id: uuid.UUID
    version: uuid.UUID = Field(default_factory=uuid.uuid7)
