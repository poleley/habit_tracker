from uuid import UUID, uuid4

from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, declarative_mixin


@declarative_mixin
class IdMixin:
    """Миксин для добавления UUID поля."""

    uuid: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        sort_order=-99,
    )


@declarative_mixin
class TimestampMixin:
    """Миксин для добавления полей времени создания и обновления."""

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        sort_order=99,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        sort_order=99,
    )


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


class User(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    habits: Mapped[list["Habit"]] = relationship(back_populates="user")


class Habit(Base, IdMixin, TimestampMixin):
    __tablename__ = "habits"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    # is_quantifiable: Mapped[bool] = mapped_column(
    #     Boolean, default=False
    # )  # True для количественных привычек
    # target_quantity: Mapped[float | None] = mapped_column(
    #     Float, nullable=True
    # )  # Целевое значение для количественных привычек
    # unit: Mapped[str | None] = mapped_column(
    #     String, nullable=True
    # )  # Единицы измерения (например, "л", "шаги")
    user: Mapped["User"] = relationship(back_populates="habits")
    # logs: Mapped[list["HabitLog"]] = relationship(back_populates="habit")


# class HabitLog(Base, IdMixin, TimestampMixin):
#     __tablename__ = "habit_logs"
#
#     habit_id: Mapped[str] = mapped_column(ForeignKey("habits.id"), nullable=False)
#     date: Mapped[datetime.datetime] = mapped_column(
#         DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False
#     )
#     is_completed: Mapped[bool | None] = mapped_column(
#         Boolean, nullable=True
#     )  # Для привычек "да/нет"
#     quantity: Mapped[float | None] = mapped_column(
#         Float, nullable=True
#     )  # Для количественных привычек
#     habit: Mapped["Habit"] = relationship(back_populates="logs")