from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.repositories.abc_uow import AbstractUnitOfWork
from app.core.settings import settings
from app.online_loan.repositories.sqlalchemy.repositories import (
    LeadPhotosRepository,
    LeadsRepository,
)

engine = create_async_engine(settings.database_url)
pg_async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class UnitOfWork(AbstractUnitOfWork):
    """Realization UnitOfWork."""

    def __init__(self, session_factory: async_sessionmaker):
        """Init for UnitOfWork."""
        self.session = session_factory()

    async def __aenter__(self):
        """Асинхронны вход в сессию."""
        self.leads = LeadsRepository(self.session)
        self.lead_photos = LeadPhotosRepository(self.session)

    async def __aexit__(self, *args):
        """Асинхронны выход из сессии."""
        await self.rollback()
        await self.session.close()

    async def commit(self):
        """Коммит."""
        await self.session.commit()

    async def rollback(self):
        """Откат изменений."""
        await self.session.rollback()
