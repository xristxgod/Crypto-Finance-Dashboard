from typing import Generic, TypeVar, Type, Optional, Any, NoReturn

from fastapi.requests import Request
from pydantic import BaseModel, UUID4

__all__ = (
    'BaseModelDB',
    'BaseManager',
    'ModelDB',
)


class BaseModelDB(BaseModel):

    class Config:
        orm_mode = True


ModelDB = TypeVar("ModelDB", bound=BaseModelDB)


class BaseDatabase(Generic[ModelDB]):
    db_model: Type[ModelDB]

    def __init__(self, db_model: Type[ModelDB]):
        self.db_model = db_model

    async def get(self, id: int | str | UUID4) -> Optional[ModelDB]:
        raise NotImplementedError()

    async def create(self, model: ModelDB) -> ModelDB:
        raise NotImplementedError()

    async def update(self, model: ModelDB) -> ModelDB:
        raise NotImplementedError()

    async def delete(self, model: ModelDB) -> None:
        raise NotImplementedError()


class BaseManager(Generic[ModelDB]):
    db_model: Type[ModelDB]

    db: BaseDatabase[ModelDB]

    class DoesNotExists(Exception):
        pass

    def __init__(self, db_model: BaseDatabase[ModelDB]):
        self.db = db_model

    async def get(self, id: int | str | UUID4) -> Optional[ModelDB]:
        model = await self.db.get(id)

        if model is None:
            raise self.DoesNotExists()

        return model

    async def create(self, model: ModelDB, request: Optional[Request] = None) -> ModelDB:
        db_model = self.db_model(**model.dict())

        created_model = await self.db.create(db_model)

        await self.on_after_create(created_model, request=request)

        return created_model

    async def on_after_create(self, created_model: ModelDB, request: Optional[Request] = None) -> NoReturn:
        pass

    async def update(self, body: BaseModel, model: ModelDB, request: Optional[Request] = None) -> ModelDB:
        update_model_dict = body.dict()

        for field in update_model_dict:
            setattr(model, field, update_model_dict[field])

        updated_model = await self.db.update(model, request=request)

        await self.on_after_update()

        return updated_model

    async def on_after_update(self, model: ModelDB, update_dict: dict[str, Any],
                              request: Optional[Request] = None) -> NoReturn:
        pass

    async def delete(self, model: ModelDB, request: Optional[Request] = None) -> NoReturn:
        await self.db.delete(model)
        await self.on_after_delete(model, request=request)

    async def on_after_delete(self, model: ModelDB, request: Optional[Request] = None) -> NoReturn:
        pass
