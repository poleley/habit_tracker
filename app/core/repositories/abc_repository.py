import abc
import uuid
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

AnyModel = Dict[str, Any]
Entity = BaseModel
FindAllResult = Tuple[int, List[Entity]]


class AbstractRepository(abc.ABC):
    """Абстрактный базовый класс для репозиториев."""

    @abc.abstractmethod
    async def add_one(self, data: AnyModel) -> Entity:
        """Добавить одну сущность."""

    @abc.abstractmethod
    async def add_one_nr(self, data: AnyModel) -> bool:
        """Добавить одну сущность без возврата результата."""

    @abc.abstractmethod
    async def add_many(self, data: List[AnyModel]) -> bool:
        """Добавить несколько сущностей."""

    @abc.abstractmethod
    async def edit_one(self, uuid: uuid.UUID, data: AnyModel) -> bool:
        """Редактировать одну сущность."""

    @abc.abstractmethod
    async def find_one(self, filter_by: AnyModel) -> Optional[Entity]:
        """Найти одну сущность по фильтру."""

    @abc.abstractmethod
    async def get_for_subname(self, name: str) -> List[Entity]:
        """Получить сущности по части имени."""

    @abc.abstractmethod
    async def find_all_pg(
        self, filter_by: AnyModel, limit: int, page: int
    ) -> FindAllResult:
        """Найти все сущности с пагинацией."""

    @abc.abstractmethod
    async def find_all(self, filter_by: AnyModel) -> FindAllResult:
        """Найти все сущности с пагинацией."""

    @abc.abstractmethod
    async def delete_with_id(self, uuid: uuid.UUID) -> bool:
        """Удалить сущность по UUID."""
