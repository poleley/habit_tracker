from collections.abc import Iterable
from typing import Any, Generic, TypeAlias, TypeVar

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

ModelType = TypeVar("ModelType")
Statement: TypeAlias = Any


class SessionHelper(Generic[ModelType]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute(self, stmt: Any) -> Any:
        return await self.session.execute(stmt)

    async def save(self, instance: Any) -> None:
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def one(self, stmt: Any) -> ModelType | None:
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()  # type: ignore

    async def all(self, stmt: Any) -> list[ModelType]:
        result = await self.session.execute(stmt)
        return result.scalars().all()  # type: ignore

    async def add(self, instance: Any) -> None:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance, ["uuid"])

    async def add_many(self, instances: list[Any]) -> None:
        self.session.add_all(instances)

    async def update(self, instance: Any) -> None:
        merged_instance = await self.session.merge(
            instance
        )
        await self.session.flush()
        await self.session.refresh(merged_instance)

    async def delete(self, instance: Any) -> None:
        await self.session.delete(instance)
        await self.session.flush()

