import uuid

from models._base import BaseMongoManager
from models.token_version import TokenVersion


class TokenVersionService:
    def __init__(self, token_version_mongo_manager: BaseMongoManager[TokenVersion]) -> None:
        self.token_version_mongo_manager = token_version_mongo_manager

    async def _get_token_version_from_db(self, user_id: uuid.UUID) -> TokenVersion:
        token_version = await self.token_version_mongo_manager.get(query={"user_id": user_id})
        if token_version is None:
            token_version = TokenVersion(user_id=user_id)
            await self.token_version_mongo_manager.create(token_version)
        return token_version

    async def get_token_version(self, user_id: uuid.UUID) -> uuid.UUID:
        token_version = await self._get_token_version_from_db(user_id=user_id)
        return token_version.version

    async def update_token_version(self, user_id: uuid.UUID) -> TokenVersion:
        token_version = await self._get_token_version_from_db(user_id=user_id)
        token_version.version = uuid.uuid7()
        await self.token_version_mongo_manager.update_by_id(token_version.id, {"version": token_version.version})
        return token_version
