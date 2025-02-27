import pytest

from habits import commands
from habits.adapters.postgresql import models

pytestmark = [
    pytest.mark.asyncio,
]


class TestHabitRepository:
    async def test_find_returns_habit(self, habit_repository, test_habit):
        instance = await habit_repository.find(test_habit.uuid)
        
        assert isinstance(instance, models.Habit)
        assert instance.uuid == test_habit.uuid
        
    # async def test_save_creates_new_habit(self, habit_repository, uow, test_user):
        # habit_data = commands.AddHabit(
        #     user_id=test_user.uuid,
        #     name="Новая привычка",
        #     description="Описание привычки"
        # )
        #
        # result = await habit_repository.save(habit_data)
        # await uow.commit()
        #
        # assert isinstance(result, models.Habit)
        # assert result.name == habit_data.name
        # assert result.description == habit_data.description
