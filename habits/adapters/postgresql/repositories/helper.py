from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType")


class SessionHelper(Generic[ModelType]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, instance: Any) -> None:
        self.session.add(instance)
        await self.session.flush()

    async def one(self, stmt: Any) -> ModelType:
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()  # type: ignore
