from typing import Annotated, TypeAlias
from uuid import UUID

from pydantic import BaseModel, StringConstraints

Name: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=100)]
Description: TypeAlias = Annotated[str, StringConstraints(max_length=1000)]
Email: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=100)]
Username: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=100)]


class AddHabit(BaseModel):
    user_id: UUID
    name: Name
    description: Description


class AddUser(BaseModel):
    name: Name
    email: Email
    username: Username
