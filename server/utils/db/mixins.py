from uuid import UUID, uuid4

from sqlalchemy.orm import MappedColumn, mapped_column


class UUIDIdMixin:
    id: MappedColumn[UUID] = mapped_column(primary_key=True, default=uuid4)
