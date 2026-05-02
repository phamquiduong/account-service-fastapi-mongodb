import uuid
from typing import Any, ClassVar, Generic, Literal, TypeVar

from pydantic import BaseModel, Field
from pymongo import AsyncMongoClient, ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.results import DeleteResult, InsertManyResult, InsertOneResult, UpdateResult

_T = TypeVar("_T", bound="MongoModel")
_SortDirection = Literal[1, -1]


class MongoModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid7, examples=["019de957-3ff8-7734-996b-b4c50d5109cd"])

    __collection_name__: ClassVar[str]

    def model_dump_mongodb(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["_id"] = data.pop("id")
        return data

    @classmethod
    def model_validate_mongodb(cls, data: dict[str, Any]):
        data["id"] = data.pop("_id")
        return cls.model_validate(data)


class BaseMongoManager(Generic[_T]):
    def __init__(self, client, db_name: str, model: type[_T]):
        self.client = client
        self.db = self.client[db_name]
        self.collection: AsyncCollection = self.db[model.__collection_name__]
        self.model = model

    @classmethod
    def from_uri(cls, uri: str, db_name: str, model: type[_T]):
        client = AsyncMongoClient(uri, uuidRepresentation="standard")
        return cls(client, db_name, model)

    async def create(self, obj: _T) -> InsertOneResult:
        data = obj.model_dump_mongodb()
        return await self.collection.insert_one(data)

    async def insert_many(self, objs: list[_T]) -> InsertManyResult:
        data = [obj.model_dump_mongodb() for obj in objs]
        return await self.collection.insert_many(data)

    async def get(self, query: dict[str, Any]) -> _T | None:
        data = await self.collection.find_one(query)
        return self.model.model_validate_mongodb(data) if data else None

    async def get_by_id(self, id_value: Any) -> _T | None:
        return await self.get({"_id": id_value})

    async def list(
        self,
        query: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 100,
        sort: list[tuple[str, _SortDirection]] | None = None,
    ) -> list[_T]:
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

    async def update_by_id(self, id_value: Any, update_data: dict[str, Any]) -> UpdateResult:
        return await self.update_one(query={"_id": id_value}, update_data=update_data)

    async def update_many(self, query: dict[str, Any], update_data: dict[str, Any]) -> UpdateResult:
        return await self.collection.update_many(query, {"$set": update_data})

    async def find_one_and_update(self, query: dict[str, Any], update_data: dict[str, Any]) -> _T | None:
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
