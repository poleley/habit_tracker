import uuid
from typing import Any, List, Optional, Type

from pydantic import BaseModel
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exc
from app.core.exc import AlreadyExists, NotFoundError
from app.core.repositories.abc_repository import (
    AbstractRepository,
    AnyModel,
    Entity,
    FindAllResult,
)


class SQLAlchemyRepository(AbstractRepository):
    """Репозиторий, реализующий CRUD-операции с базой данных через SQLAlchemy.

    Позволяет взаимодействовать с моделью базы данных с использованием асинхронных сессий.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: Any,
        schema: Optional[Type[BaseModel]] = None,
    ):
        """
        Инициализация репозитория.

        :param session: Асинхронная сессия SQLAlchemy.
        :param model: Модель базы данных для работы с таблицей.
        :param schema: Pydantic-схема для сериализации и десериализации данных.
        """
        self.session = session
        self.model = model
        self.schema = schema
        self.name = self.model.__name__

    async def add_one(self, data: AnyModel) -> Entity:
        """
        Добавляет одну запись в базу данных и возвращает её.

        :param data: Данные для вставки.
        :return: Экземпляр модели базы данных.
        """
        try:
            stmt = insert(self.model).values(**data).returning(self.model)
            result = await self.session.execute(stmt)
            instance = result.scalar_one()
            return self.to_read_model(instance)
        except IntegrityError as e:
            self.handle_integrity_error(e)

    async def add_one_nr(self, data: AnyModel) -> bool:
        """
        Добавляет одну запись в базу данных без возврата результата.

        :param data: Данные для вставки.
        :return: True при успешной вставке, иначе ошибка.
        """
        try:
            stmt = insert(self.model).values(**data)
            await self.session.execute(stmt)
            return True
        except IntegrityError as e:
            self.handle_integrity_error(e)

    async def add_many(self, data: List[AnyModel]) -> bool:
        """
        Добавляет несколько записей в базу данных.

        :param data: Список данных для вставки.
        :return: True при успешной вставке, иначе ошибка.
        """
        try:
            stmt = pg_insert(self.model).values(data).on_conflict_do_nothing()
            await self.session.execute(stmt)
            return True
        except IntegrityError as e:
            self.handle_integrity_error(e)

    async def edit_one(self, uuid: uuid.UUID, data: AnyModel) -> bool:
        """
        Обновляет запись в базе данных по её UUID.

        :param uuid: UUID записи для обновления.
        :param data: Данные для обновления.
        :return: True при успешном обновлении, иначе ошибка.
        """
        stmt = update(self.model).where(self.model.uuid == uuid).values(**data)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise exc.NotFoundError(f"{self.name} не найден")
        return True

    async def find_one(self, filter_by: AnyModel) -> Entity:
        """
        Ищет одну запись в базе данных по фильтру.

        :param filter_by: Фильтр для поиска.
        :return: Экземпляр модели или None, если запись не найдена.
        """
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if not instance:
            raise exc.NotFoundError()
        return self.to_read_model(instance)

    async def get_for_subname(self, name: str) -> List[Entity]:
        """
        Ищет записи по частичному совпадению имени.

        :param name: Строка для поиска по имени.
        :return: Список найденных сущностей.
        """
        stmt = select(self.model).where(self.model.name.ilike(f"%{name}%"))
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self.to_read_model(instance) for instance in instances]

    async def find_all(self, filter_by: AnyModel) -> FindAllResult:
        """
        Ищет все записи по фильтру.

        :param filter_by: Фильтр для поиска.
        :return: Общее количество записей и список сущностей.
        """
        stmt = select(self.model).filter_by(**filter_by)
        count_stmt = select(func.count(self.model.uuid)).filter_by(**filter_by)

        total_count = (await self.session.execute(count_stmt)).scalar_one()
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return total_count, [self.to_read_model(instance) for instance in instances]

    async def find_all_pg(
        self, filter_by: AnyModel, limit: int, page: int
    ) -> FindAllResult:
        """
        Пагинированный поиск записей по фильтру.

        :param filter_by: Фильтр для поиска.
        :param limit: Лимит на количество записей.
        :param page: Номер страницы.
        :return: Общее количество записей и список сущностей.
        """
        offset = (page - 1) * limit
        stmt = select(self.model).filter_by(**filter_by).limit(limit).offset(offset)
        count_stmt = select(func.count(self.model.uuid)).filter_by(**filter_by)

        total_count = (await self.session.execute(count_stmt)).scalar_one()
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return total_count, [self.to_read_model(instance) for instance in instances]

    async def delete_with_id(self, uuid: uuid.UUID) -> bool:
        """
        Удаляет запись по её UUID.

        :param uuid: UUID записи для удаления.
        :return: True при успешном удалении, иначе ошибка.
        """
        stmt = delete(self.model).where(self.model.uuid == uuid)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise exc.NotFoundError(f"{self.name} не найден")
        return True

    def to_read_model(self, obj: Any) -> Entity:
        """
        Преобразует ORM объект в модель pydantic для сериализации.

        :param obj: ORM объект.
        :return: Модель pydantic или сам объект, если схема не указана.
        """
        if self.schema:
            return self.schema.model_validate(obj, from_attributes=True)
        return obj

    def handle_integrity_error(self, e: IntegrityError) -> None:
        """
        Обрабатывает ошибки целостности данных (например, нарушение уникальности).

        :param e: Исключение IntegrityError.
        :raises AlreadyExists: Если запись с такими данными уже существует.
        :raises NotFoundError: Если связанный объект не найден.
        """
        if hasattr(e.orig, "pgcode"):
            if e.orig.pgcode == "23503":  # foreign_key_violation
                raise NotFoundError("Связанный объект не найден.")
            elif e.orig.pgcode == "23505":  # unique_violation
                raise AlreadyExists(f"{self.name} уже существует.")
        raise e
