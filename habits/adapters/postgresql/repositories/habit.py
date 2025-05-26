import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from habits import commands, entities
from habits.adapters.postgresql import models
from habits.adapters.postgresql.repositories.helper import SessionHelper
from habits.adapters.postgresql.registry import mapper


class HabitRepository:
    def __init__(self, session: AsyncSession):
        self.helper = SessionHelper[models.Habit](session)

    async def get_all_by_user(self, user_id: UUID) -> list[entities.Habit]:
        stmt = select(models.Habit).where(models.Habit.user_id == user_id)
        return [mapper.map(instance, entities.Habit) for instance in await self.helper.all(stmt)]

    async def find(self, uuid: UUID) -> entities.Habit | None:
        stmt = select(models.Habit).where(models.Habit.uuid == uuid)
        instance = await self.helper.one(stmt)
        if instance:
            return mapper.map(instance, entities.Habit)

    async def add_one(self, new_habit: entities.Habit) -> entities.Habit:
        habit = await self.helper.save(mapper.map(new_habit, models.Habit))
        return mapper.map(habit, entities.Habit)


    async def delete(self, habit: entities.Habit) -> None:
        await self.helper.delete(mapper.map(habit, models.Habit))


class HabitLogRepository:
    def __init__(self, session: AsyncSession):
        self.helper = SessionHelper[models.HabitLog](session)

    async def get_logs_by_user(self, user_id: UUID) -> list[models.HabitLog]:
        stmt = select(models.HabitLog).join(models.Habit).where(models.Habit.user_id == user_id)
        return await self.helper.all(stmt)

    async def get_by_habit_and_date(self, habit_id: UUID, log_date: datetime.datetime) -> models.HabitLog | None:
        stmt = select(models.HabitLog).where(
            models.HabitLog.habit_id == habit_id,
            models.HabitLog.date == log_date,
        )
        return await self.helper.one(stmt)

    async def add_one(self, new_habit_log: entities.HabitLog) -> entities.HabitLog:
        habit_log = await self.helper.save(mapper.map(new_habit_log, models.HabitLog))
        return mapper.map(habit_log, entities.HabitLog)

    async def delete(self, log: entities.HabitLog) -> None:
        await self.helper.delete(mapper.map(log, models.HabitLog))