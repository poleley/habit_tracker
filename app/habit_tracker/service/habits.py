from app.core.repositories.abc_uow import AbstractUnitOfWork


class HabitsService:
    def __init__(self, uow: AbstractUnitOfWork):
        """
        Инициализация сервиса с использованием Unit of Work.

        :param uow: Абстрактный класс для работы с репозиторием и транзакциями.
        """
        self.uow = uow
