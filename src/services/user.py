import logging
import uuid

from pydantic import EmailStr

from models._base import BaseMongoManager
from models.user import User
from utils.password import get_password_hash, verify_password

_logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_mongo_manager: BaseMongoManager[User]):
        self.user_mongo_manager = user_mongo_manager

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.user_mongo_manager.get_by_id(id_value=user_id)

    async def get_by_email(self, email: EmailStr) -> User | None:
        return await self.user_mongo_manager.get(query={"email": email})

    async def update_password(self, user_id: uuid.UUID, new_password: str):
        new_password_hashed = get_password_hash(new_password)
        await self.user_mongo_manager.update_by_id(user_id, {"password": new_password_hashed})

    async def list(self, skip: int, limit: int) -> list[User]:
        return await self.user_mongo_manager.list(skip=skip, limit=limit)

    async def create(self, email: EmailStr, password: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(email=email, password=hashed_password)
        await self.user_mongo_manager.create(user)
        return user

    async def authenticate_user(self, email: EmailStr, password: str) -> User | None:
        user = await self.get_by_email(email=email)

        if user is None:
            _logger.warning("user with email [%s] does not exist", email)
            return None

        if verify_password(plain_password=password, hashed_password=user.password) is False:
            _logger.warning("user with email [%s] wrong password", email)
            return None

        return user
