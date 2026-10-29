from typing import TypeVar, Generic
from beanie import Document, PydanticObjectId

ModelType = TypeVar("ModelType", bound=Document)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_one(self, **filters):
        return await self.model.find_one(filters)

    async def get_by_id(self, id: str) -> ModelType | None:
        return await self.model.find_one({"_id": PydanticObjectId(id)})

    async def get_filtered(self, **filters) -> list[ModelType]:
        return await self.model.find(filters).to_list()

    async def get_all(self) -> list[ModelType]:
        return await self.get_filtered()

    async def add(self, data: dict) -> ModelType:
        instance = self.model(**data)
        await instance.insert()
        return instance

    async def delete(self, id: str) -> None:
        await self.model.delete_one({"_id": PydanticObjectId(id)})

    async def edit(self, id: str, data: dict) -> None:
        await self.model.update_one({"_id": PydanticObjectId(id)}, {"$set": data})