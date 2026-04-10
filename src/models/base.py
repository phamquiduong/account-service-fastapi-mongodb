from typing import Any, Generic, Literal, TypeVar

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import AsyncMongoClient, ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection

T = TypeVar("T", bound="MongoModel")
SortDirection = Literal[1, -1]


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        from pydantic_core import core_schema

        return core_schema.str_schema()

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


class MongoModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }


class BaseMongoManager(Generic[T]):
    def __init__(self, uri: str, db_name: str, collection_name: str, model: type[T]):
        self.client = AsyncMongoClient(uri)
        self.db = self.client[db_name]
        self.collection: AsyncCollection = self.db[collection_name]
        self.model = model

    async def create(self, obj: T) -> T:
        data = obj.model_dump(by_alias=True)
        await self.collection.insert_one(data)
        return obj

    async def insert_many(self, objs: list[T]) -> list[T]:
        data = [obj.model_dump(by_alias=True) for obj in objs]
        await self.collection.insert_many(data)
        return objs

    async def get(self, query: dict[str, Any]) -> T | None:
        data = await self.collection.find_one(query)
        return self.model.model_validate(data) if data else None

    async def list(
        self,
        query: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 100,
        sort: list[tuple[str, SortDirection]] | None = None,
    ) -> list[T]:
        cursor = self.collection.find(query)

        if sort:
            cursor = cursor.sort(sort)

        cursor = cursor.skip(skip).limit(limit)

        return [self.model.model_validate(doc) async for doc in cursor]

    async def count(self, query: dict[str, Any]) -> int:
        return await self.collection.count_documents(query)

    async def update_one(self, query: dict[str, Any], update_data: dict[str, Any], *, upsert: bool = False) -> bool:
        result = await self.collection.update_one(query, {"$set": update_data}, upsert=upsert)
        return result.modified_count > 0 or result.upserted_id is not None

    async def update_many(self, query: dict[str, Any], update_data: dict[str, Any]) -> int:
        result = await self.collection.update_many(query, {"$set": update_data})
        return result.modified_count

    async def find_one_and_update(self, query: dict[str, Any], update_data: dict[str, Any]) -> T | None:
        data = await self.collection.find_one_and_update(
            query, {"$set": update_data}, return_document=ReturnDocument.AFTER
        )
        return self.model.model_validate(data) if data else None

    async def delete_one(self, query: dict[str, Any]) -> bool:
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0

    async def delete_many(self, query: dict[str, Any]) -> int:
        result = await self.collection.delete_many(query)
        return result.deleted_count
