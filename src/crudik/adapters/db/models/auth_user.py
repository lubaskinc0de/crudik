from sqlalchemy import UUID, Column, ForeignKey, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from crudik.adapters.auth.model import AuthUser
from crudik.adapters.db.models.base import mapper_registry

auth_user_table = Table(
    "auth_user",
    mapper_registry.metadata,
    Column("auth_user_id", Text, primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    UniqueConstraint("user_id", "auth_user_id", name="uq_auth_user"),
)


mapper_registry.map_imperatively(
    AuthUser,
    auth_user_table,
    properties={
        "user": relationship("User", lazy="selectin"),
    },
)
