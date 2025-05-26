from typing import Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from habits import commands, entities
from habits.adapters.postgresql import models
from habits.adapters.postgresql.repositories.helper import SessionHelper
from habits.adapters.postgresql.registry import mapper


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.helper = SessionHelper[models.User](session)

    async def find_all(self) -> list[entities.User]:
        stmt = select(models.User)
        return [mapper.map(instance, entities.User) for instance in await self.helper.all(stmt)]

    async def find(self, filters: dict[str, Any]) -> entities.User | None:
        stmt = select(models.User).filter_by(**filters)
        instance = await self.helper.one(stmt)
        if instance:
            return mapper.map(instance, entities.User)

    async def save(self, new_user: commands.AddUserWithHashedPassword) -> entities.User:
        instance = models.User(**new_user.model_dump())
        await self.helper.save(instance)
        return mapper.map(instance, entities.User)

    async def delete(self, user: entities.User) -> None:
        await self.helper.delete(mapper.map(user, models.User))
