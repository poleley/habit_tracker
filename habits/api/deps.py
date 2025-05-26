import functools

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from habits.adapters.database import AsyncDatabase
from habits.adapters.postgresql.repositories.habit import HabitRepository
from habits.adapters.postgresql.repositories.unitofwork import UnitOfWork
from habits.adapters.postgresql.repositories.user import UserRepository
from habits.settings import settings
from habits.usecases.habit import AddHabitUseCase
from habits.usecases.user import AddUserUseCase, GetUsersUseCase, LoginUserUseCase


@functools.lru_cache()
def get_database() -> AsyncDatabase:
    return AsyncDatabase(pg_dsn=str(settings.database_url))


async def get_session(database: AsyncDatabase = Depends(get_database)):
    async with database.session() as session:
        yield session


async def get_habit_repository(
    session: AsyncSession = Depends(get_session),
) -> HabitRepository:
    return HabitRepository(session)


async def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


async def get_unit_of_work(
    session: AsyncSession = Depends(get_session),
) -> UnitOfWork:
    return UnitOfWork(session)


async def get_add_habit_use_case(
    habit_repository: HabitRepository = Depends(get_habit_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> AddHabitUseCase:
    return AddHabitUseCase(habit_repository, user_repository, uow)


async def get_get_users_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetUsersUseCase:
    return GetUsersUseCase(user_repository)


async def get_add_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> AddUserUseCase:
    return AddUserUseCase(user_repository, uow)


def get_login_user_use_case(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> LoginUserUseCase:
    return LoginUserUseCase(uow)
