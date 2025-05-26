from dataclasses import dataclass
from uuid import UUID


@dataclass(kw_only=True)
class Status:
    uuid: UUID
    name: str
    code: str


@dataclass(kw_only=True)
class City:
    uuid: UUID
    name: str
    code: int
