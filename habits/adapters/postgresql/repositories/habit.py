from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from habits import views, commands
from habits.adapters.postgresql import models
from habits.adapters.postgresql.repositories.helper import SessionHelper


class HabitRepository:
    def __init__(self, session: AsyncSession):
        self.helper = SessionHelper[models.Habit](session)

    async def find(self, uuid: UUID) -> views.Habit:
        stmt = select(models.Habit).filter_by(uuid=uuid)
        instance = await self.helper.one(stmt)
        return instance

    async def save(self, new_habit: commands.AddHabit) -> views.Habit:
        instance = models.Habit(**new_habit.model_dump())
        await self.helper.save(instance)
        return views.Habit.model_validate(instance)

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.helper = SessionHelper[models.User](session)

    async def find(self, uuid: UUID) -> views.User:
        stmt = select(models.User).filter_by(uuid=uuid)
        instance = await self.helper.one(stmt)
        return instance

    async def save(self, new_habit: commands.AddHabit) -> None:
        pass