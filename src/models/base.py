from typing import Any, Generic, Literal, TypeVar

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import AsyncMongoClient, ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.results import DeleteResult, InsertManyResult, InsertOneResult, UpdateResult

T = TypeVar("T", bound="MongoModel")
SortDirection = Literal[1, -1]


class MongoModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))

    def model_dump_mongodb(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["_id"] = ObjectId(data.pop("id"))
        return data

    @classmethod
    def model_validate_mongodb(cls, data: dict[str, Any]):
        data["id"] = str(data.pop("_id"))
        return cls.model_validate(data)


class BaseMongoManager(Generic[T]):
    def __init__(self, uri: str, db_name: str, collection_name: str, model: type[T]):
        self.client = AsyncMongoClient(uri)
        self.db = self.client[db_name]
        self.collection: AsyncCollection = self.db[collection_name]
        self.model = model

    async def create(self, obj: T) -> InsertOneResult:
        data = obj.model_dump_mongodb()
        return await self.collection.insert_one(data)

    async def insert_many(self, objs: list[T]) -> InsertManyResult:
        data = [obj.model_dump_mongodb() for obj in objs]
        return await self.collection.insert_many(data)

    async def get(self, query: dict[str, Any]) -> T | None:
        data = await self.collection.find_one(query)
        return self.model.model_validate_mongodb(data) if data else None

    async def list(
        self,
        query: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 100,
        sort: list[tuple[str, SortDirection]] | None = None,
    ) -> list[T]:
        cursor = self.collection.find(query or {})

        if sort:
            cursor = cursor.sort(sort)

        cursor = cursor.skip(skip).limit(limit)

        return [self.model.model_validate_mongodb(doc) async for doc in cursor]

    async def count(self, query: dict[str, Any]) -> int:
        return await self.collection.count_documents(query)

    async def update_one(
        self, query: dict[str, Any], update_data: dict[str, Any], upsert: bool = False
    ) -> UpdateResult:
        return await self.collection.update_one(query, {"$set": update_data}, upsert=upsert)

    async def update_many(self, query: dict[str, Any], update_data: dict[str, Any]) -> UpdateResult:
        return await self.collection.update_many(query, {"$set": update_data})

    async def find_one_and_update(self, query: dict[str, Any], update_data: dict[str, Any]) -> T | None:
        data = await self.collection.find_one_and_update(
            query, {"$set": update_data}, return_document=ReturnDocument.AFTER
        )

        if not data:
            return None

        return self.model.model_validate_mongodb(data)

    async def delete_one(self, query: dict[str, Any]) -> DeleteResult:
        return await self.collection.delete_one(query)

    async def delete_many(self, query: dict[str, Any]) -> DeleteResult:
        return await self.collection.delete_many(query)
