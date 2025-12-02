from typing import override

from crudik.adapters.db.gateway.base import SAGateway
from crudik.application.common.gateway.user import UserGateway
from crudik.entities.identifiers import UserId
from crudik.entities.user import User


class SAUserGateway(UserGateway, SAGateway):
    @override
    async def get(self, user_id: UserId) -> User | None:
        return await self._session.get(User, user_id)
