from typing import Annotated, TypeAlias
from uuid import UUID

from pydantic import BaseModel, StringConstraints

Name: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=100)]
Description: TypeAlias = Annotated[str, StringConstraints(max_length=1000)]
Email: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=100)]
Username: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=100)]
Password: TypeAlias = Annotated[str, StringConstraints(min_length=8, max_length=100)]


class AddHabit(BaseModel):
    user_uuid: UUID
    name: Name
    description: Description


class AddUser(BaseModel):
    username: Username
    email: Email
    password: Password


class AddUserWithHashedPassword(BaseModel):
    username: Username
    email: Email
    hashed_password: str


class LoginUser(BaseModel):
    username: Username
    password: Password
