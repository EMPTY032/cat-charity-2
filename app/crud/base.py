from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType]):

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> ModelType | None:
        return await session.get(self.model, obj_id)

    async def get_multi(
        self,
        session: AsyncSession
    ) -> list[ModelType]:
        result = await session.execute(
            select(self.model)
        )
        return list(result.scalars().all())

    async def create(
        self,
        obj_in: BaseModel,
        session: AsyncSession
    ) -> ModelType:
        obj_data = obj_in.model_dump()

        db_obj = self.model(**obj_data)

        session.add(db_obj)
        await session.flush()

        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: BaseModel,
        session: AsyncSession,
    ) -> ModelType:

        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.flush()

        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:

        await session.delete(db_obj)
        await session.flush()

        return db_obj