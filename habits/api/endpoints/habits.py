from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, status, HTTPException

from habits import commands, views
from habits.adapters.postgresql.repositories.habit import HabitRepository
from habits.api import deps
from habits.usecases.habit import AddHabitUseCase, GetHabitUseCase

router = APIRouter()


@router.post("/habits", status_code=status.HTTP_201_CREATED)
async def add_habit(
    command: commands.AddHabit = Body(),
    add_habit_use_case: AddHabitUseCase = Depends(deps.get_add_habit_use_case),
) -> views.Habit:
    return await add_habit_use_case(command)


@router.get("/habits")
async def get_habits():
    pass


@router.get("/habit-logs")
async def get_my_habit_logs():
    pass


@router.post("/habit-logs/{habit_id}")
async def create_habit_log(
    habit_id: UUID = Path(..., description="UUID of the habit"),
):
    pass


@router.delete("/habit-logs/{habit_id}")
async def delete_habit_log(
    habit_id: UUID = Path(..., description="UUID of the habit"),
):
    pass


@router.get("/users/me/statistics")
async def get_habit_statistics():
    pass


@router.get("/habits/{uuid}")
async def get_habit(
    uuid: UUID = Path(),
    habit_repository: HabitRepository = Depends(
        deps.get_habit_repository
    ),
) -> views.Habit:
    get_habit = GetHabitUseCase(habit_repository)
    return await get_habit(uuid)
