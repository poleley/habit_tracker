from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Habit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    user_id: UUID
    name: str
    description: str | None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    username: str
    email: str
