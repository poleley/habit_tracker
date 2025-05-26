from uuid import UUID

from fastapi import APIRouter, Body, Depends, status

from habits import commands, views
from habits.api import deps
from habits.usecases.user import AddUserUseCase, GetUsersUseCase

router = APIRouter()


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    get_users_use_case: GetUsersUseCase = Depends(deps.get_get_users_use_case),
) -> list[views.User]:
    return await get_users_use_case()


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def add_user(
    command: commands.AddUser = Body(),
    add_user_use_case: AddUserUseCase = Depends(deps.get_add_user_use_case),
) -> views.User:
    return await add_user_use_case(command)

