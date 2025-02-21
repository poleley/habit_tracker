from typing import Annotated, TypeAlias
from uuid import UUID

from pydantic import BaseModel, StringConstraints

Name: TypeAlias = Annotated[str, StringConstraints(min_length=1, max_length=100)]
Description: TypeAlias = Annotated[str, StringConstraints(max_length=1000)]


class AddHabit(BaseModel):
    user_id: UUID
    name: Name
    description: Description
