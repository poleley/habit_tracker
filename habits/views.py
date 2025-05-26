import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Habit(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    uuid: UUID
    user_uuid: UUID
    name: str
    description: str | None
    is_quantifiable: bool
    target_quantity: float | None
    unit: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    uuid: UUID
    username: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

