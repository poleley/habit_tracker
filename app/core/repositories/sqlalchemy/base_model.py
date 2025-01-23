import uuid as uuid_module
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_mixin, mapped_column


@declarative_mixin
class UuidMixin:
    """Миксин для добавления UUID поля."""

    uuid: Mapped[uuid_module.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_module.uuid4,
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
