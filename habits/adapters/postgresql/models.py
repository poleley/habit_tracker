import datetime

from sqlalchemy import ForeignKey, String, func, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from habits.core.base_model import Base, IdMixin, TimestampMixin


class User(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    habits: Mapped[list["Habit"]] = relationship(back_populates="user")


class Habit(Base, IdMixin, TimestampMixin):
    __tablename__ = "habits"

    user_uuid: Mapped[str] = mapped_column(ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
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


class HabitLog(Base, IdMixin, TimestampMixin):
    __tablename__ = "habit_logs"

    habit_uuid: Mapped[str] = mapped_column(ForeignKey("habits.uuid", ondelete="CASCADE"), nullable=False)
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