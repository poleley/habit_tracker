import abc

from app.core.repositories.abc_repository import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    """Абстрактный класс UOW."""

    leads: AbstractRepository
    lead_photos: AbstractRepository

    @abc.abstractmethod
    async def __aenter__(self):
        """Abstract method."""
        raise NotImplementedError

    @abc.abstractmethod
    async def __aexit__(self, *args):
        """Abstract method."""
        raise NotImplementedError

    @abc.abstractmethod
    async def commit(self):
        """Abstract method."""
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        """Abstract method."""
        raise NotImplementedError
