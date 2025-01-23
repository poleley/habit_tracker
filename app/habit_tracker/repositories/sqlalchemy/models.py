import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.repositories.sqlalchemy.base_model import Base, TimestampMixin, UuidMixin


class User(Base, UuidMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    habits: Mapped[list["Habit"]] = relationship(back_populates="user")


class Habit(Base, UuidMixin, TimestampMixin):
    __tablename__ = "habits"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    is_quantifiable: Mapped[bool] = mapped_column(
        Boolean, default=False
    )  # True для количественных привычек
    target_quantity: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Целевое значение для количественных привычек
    unit: Mapped[str | None] = mapped_column(
        String, nullable=True
    )  # Единицы измерения (например, "л", "шаги")
    user: Mapped["User"] = relationship(back_populates="habits")
    logs: Mapped[list["HabitLog"]] = relationship(back_populates="habit")


class HabitLog(Base, UuidMixin, TimestampMixin):
    __tablename__ = "habit_logs"

    habit_id: Mapped[str] = mapped_column(ForeignKey("habits.id"), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    is_completed: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Для привычек "да/нет"
    quantity: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Для количественных привычек
    habit: Mapped["Habit"] = relationship(back_populates="logs")
