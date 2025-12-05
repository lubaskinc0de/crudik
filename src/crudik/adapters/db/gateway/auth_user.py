from typing import override

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.adapters.auth.common.gateway.auth_user import AuthUserGateway
from crudik.adapters.auth.model import AuthUser, AuthUserId
from crudik.adapters.db.models.auth_user import auth_user_table


class SAAuthUserGateway(AuthUserGateway):
    """SQLAlchemy-based implementation of AuthUserGateway for managing authentication user records in the database."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def is_exists(self, auth_user_id: AuthUserId) -> bool:
        """Checks whether an authentication user record exists in the database for the given auth user ID."""
        return (
            await self._session.execute(
                select(exists().where(auth_user_table.c.auth_user_id == auth_user_id)),
            )
        ).scalar_one()

    @override
    async def get(self, auth_user_id: AuthUserId) -> AuthUser | None:
        """Retrieves an authentication user entity from the database by auth user ID, returns None if not found."""
        return await self._session.get(AuthUser, auth_user_id)
