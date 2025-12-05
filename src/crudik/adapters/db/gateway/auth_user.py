from typing import override

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.adapters.auth.common.gateway.auth_user import AuthUserGateway
from crudik.adapters.auth.model import AuthUserId
from crudik.adapters.db.models.auth_user import auth_user_table


class SAAuthUserGateway(AuthUserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def is_exists(self, auth_user_id: AuthUserId) -> bool:
        return (
            await self._session.execute(
                select(exists().where(auth_user_table.c.auth_user_id == auth_user_id)),
            )
        ).scalar_one()
