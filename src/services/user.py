from pydantic import EmailStr

from dependencies.repositories.user import UserRepositoryDep
from models.user import User
from utils.password import get_password_hash


class UserService:
    def __init__(self, user_repository: UserRepositoryDep):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.user_repository.get_by_id(id_value=user_id)

    async def get_by_email(self, email: EmailStr) -> User | None:
        return await self.user_repository.get(query={"email": email})

    async def update_password(self, user_id: str, new_password: str):
        new_password_hashed = get_password_hash(new_password)
        await self.user_repository.update_by_id(user_id, {"password": new_password_hashed})

    async def list(self, skip: int, limit: int) -> list[User]:
        return await self.user_repository.list(skip=skip, limit=limit)

    async def create(self, email: EmailStr, password: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(email=email, password=hashed_password)
        await self.user_repository.create(user)
        return user
