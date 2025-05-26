from dataclasses import dataclass

from fastapi import HTTPException, status
from habits import commands, errors, views
from habits.adapters.postgresql.repositories.unitofwork import UnitOfWork
from habits.adapters.postgresql.repositories.user import UserRepository
from habits.core.security import get_password_hash, verify_password, create_access_token


@dataclass
class GetUsersUseCase:
    user_repository: UserRepository

    async def __call__(self) -> list[views.User]:
        users = await self.user_repository.find_all()
        return [views.User.model_validate(user) for user in users]


class AddUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, command: commands.AddUser) -> views.User:
        async with self.uow:
            # Проверяем, существует ли пользователь с таким email или username
            try:
                await self.uow.users.find({"email": command.email})
                raise errors.AlreadyExistsError(f"User with email {command.email} already exists")
            except:
                pass

            try:
                await self.uow.users.find({"username": command.username})
                raise errors.AlreadyExistsError(f"User with username {command.username} already exists")
            except:
                pass

            # Хэшируем пароль перед сохранением
            user_data = command.model_dump()
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
            
            # Сохраняем пользователя
            user = await self.uow.users.save(user_data)
            await self.uow.commit()
            
            return views.User.model_validate(user)


class LoginUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, command: commands.LoginUser) -> dict:
        async with self.uow:
            try:
                user = await self.uow.users.find({"username": command.username})
            except:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not verify_password(command.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token = create_access_token(
                data={"sub": str(user.uuid), "username": user.username}
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
