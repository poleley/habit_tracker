import functools

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from habits.adapters.database import AsyncDatabase
from habits.adapters.postgresql.repositories.habit import HabitRepository, UserRepository
from habits.adapters.postgresql.repositories.unitofwork import UnitOfWork
from habits.settings import settings


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
