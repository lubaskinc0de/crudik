from sqlalchemy import UUID, Column, Table

from crudik.adapters.db.models.base import mapper_registry
from crudik.domain.user import User

user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
)


mapper_registry.map_imperatively(User, user_table)
