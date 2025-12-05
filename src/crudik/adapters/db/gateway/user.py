from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.common.gateway.user import UserGateway
from crudik.entities.common.identifiers import UserId
from crudik.entities.user import User


class SAUserGateway(UserGateway):
    """SQLAlchemy-based implementation of UserGateway for reading user entities from PostgreSQL database."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def get(self, user_id: UserId) -> User | None:
        """Queries the database for a user by ID using SQLAlchemy session, returns None if not found."""
        return await self._session.get(User, user_id)
