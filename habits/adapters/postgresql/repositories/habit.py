from uuid import UUID

from habits.adapters.postgresql import models
from habits.adapters.postgresql.registry import mapper
from habits.domain import entities


class HabitRepository:
    async def find(self, uuid: UUID) -> entities.Habit:
        instance = await models.Habit.get("67922aea9865f65825421a07")
        return mapper.map(instance, entities.Habit)

    async def save(self, new_habit: entities.Habit) -> None:
        pass
