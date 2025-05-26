from dataclasses import dataclass
import datetime
from uuid import UUID


@dataclass(kw_only=True)
class User:
    uuid: UUID | None = None
    email: str
    username: str
    hashed_password: str
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


@dataclass(kw_only=True)
class Habit:
    uuid: UUID | None = None
    user_id: UUID
    name: str
    description: str | None
    is_quantifiable: bool
    target_quantity: float | None
    unit: str | None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None 


@dataclass(kw_only=True)
class HabitLog:
    uuid: UUID | None = None
    habit_uuid: UUID
    date: datetime.datetime
    is_completed: bool | None
    quantity: float | None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
