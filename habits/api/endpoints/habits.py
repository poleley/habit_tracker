from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, status, HTTPException

from habits import commands, views
from habits.adapters.postgresql.repositories.habit import HabitRepository, UserRepository
from habits.adapters.postgresql.repositories.unitofwork import UnitOfWork
from habits.api import deps
from habits.errors import NotFoundError
from habits.usecases.habit import AddHabitUseCase, GetHabitUseCase

router = APIRouter()


@router.get("/habits/{uuid}")
async def get_habit(
    uuid: UUID = Path(),
    habit_repository: HabitRepository = Depends(
        deps.get_habit_repository
    ),
) -> views.Habit:
    get_habit = GetHabitUseCase(habit_repository)
    return await get_habit(uuid)


@router.post("/habits", status_code=status.HTTP_201_CREATED)
async def add_habit(
    command: commands.AddHabit = Body(),
    habit_repository: HabitRepository = Depends(
        deps.get_habit_repository
    ),
    user_repository: UserRepository = Depends(
        deps.get_user_repository
    ),
    uow: UnitOfWork = Depends(deps.get_unit_of_work),
) -> views.Habit:
    add_habit = AddHabitUseCase(
        habit_repository=habit_repository, user_repository=user_repository, uow=uow
    )
    try:
        return await add_habit(command)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
