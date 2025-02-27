import pytest
import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from habits.settings import settings
from habits.adapters.postgresql import models
from habits.adapters.postgresql.models import Base
from habits.adapters.postgresql.repositories.habit import HabitRepository, UserRepository
from habits.adapters.postgresql.repositories.helper import SessionHelper
from habits.adapters.postgresql.repositories.unitofwork import UnitOfWork


pytestmark = [pytest.mark.asyncio]


# Создаем движок для тестовой базы данных
test_engine = create_async_engine(settings.test_database_url, future=True, echo=False, poolclass=NullPool)

# Создаем фабрику сессий для тестов
TestSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


@pytest.fixture(scope="session")
async def test_db():
    """Создает тестовую БД в памяти."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose(close=True)


@pytest_asyncio.fixture
async def async_session(test_db):
    """
    Фикстура для предоставления асинхронной сессии базы данных.
    """
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def clean_tables(async_session):
    """Очищает все таблицы перед каждым тестом."""
    for table in reversed(Base.metadata.sorted_tables):
        await async_session.execute(table.delete())


@pytest.fixture
def uow(async_session):
    """Создает фикстуру для UnitOfWork."""
    return UnitOfWork(async_session)


@pytest.fixture
def habit_repository(async_session):
    """Фикстура для репозитория привычек."""
    return HabitRepository(async_session)


@pytest.fixture
def user_repository(async_session):
    """Фикстура для репозитория пользователей."""
    return UserRepository(async_session)

@pytest.fixture
def helper(async_session):
    """Фикстура для helper."""
    return SessionHelper(async_session)

@pytest_asyncio.fixture
async def test_user(helper, uow):
    instance = models.User(
        username="test",
        email="test@test.com",
        hashed_password="1234",
    )
    await helper.save(instance)
    await uow.commit()
    return instance


@pytest_asyncio.fixture
async def test_habit(helper, uow, test_user):
    instance = models.Habit(
        user_id=str(test_user.uuid),
        name="Тестовая привычка"
    )
    await helper.save(instance)
    await uow.commit()
    return instance
