from dataclasses import dataclass
from uuid import UUID

from habits.adapters.postgresql.repositories.unitofwork import UnitOfWork
from habits.adapters.postgresql.repositories.habit import HabitRepository
from habits import errors, views, commands
from habits.adapters.postgresql.repositories.user import UserRepository


@dataclass
class GetHabitUseCase:
    habit_repository: HabitRepository

    async def __call__(self, uuid: UUID) -> views.Habit:
        habit = await self.habit_repository.find(uuid=uuid)
        if habit is None:
            raise errors.NotFoundError(f"habit '{uuid}' not found")

        return views.Habit.model_validate(habit)


@dataclass
class AddHabitUseCase:
    habit_repository: HabitRepository
    user_repository: UserRepository
    uow: UnitOfWork

    async def __call__(self, command: commands.AddHabit) -> views.Habit:
        user = await self.user_repository.find(
            uuid=command.user_uuid
        )
        if user is None:
            raise errors.NotFoundError(
                detail=f"User '{command.user_uuid}' not found"
            )

        new_habit = await self.habit_repository.save(command)
        await self.uow.commit()

        return new_habit
