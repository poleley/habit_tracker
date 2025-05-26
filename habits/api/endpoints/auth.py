from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from habits import commands
from habits.api import deps
from habits.usecases.user import LoginUserUseCase

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_use_case: LoginUserUseCase = Depends(deps.get_login_user_use_case),
) -> dict:
    command = commands.LoginUser(
        username=form_data.username,
        password=form_data.password
    )
    return await login_use_case(command) 