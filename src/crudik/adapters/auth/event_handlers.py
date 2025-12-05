from typing import Any, override

from bazario.asyncio import NotificationHandler

from crudik.adapters.auth.common.gateway.auth_user import AuthUserGateway
from crudik.adapters.auth.errors.auth_user import AuthUserAlreadyExistsError
from crudik.adapters.auth.idp.base import AuthUserIdProvider
from crudik.adapters.auth.model import AuthUser
from crudik.application.common.event.user import UserCreated
from crudik.application.common.uow import UoW


class UserCreatedHandler(NotificationHandler[UserCreated]):
    def __init__(self, *args: Any, uow: UoW, idp: AuthUserIdProvider, gateway: AuthUserGateway, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._uow = uow
        self._idp = idp
        self._gateway = gateway

    @override
    async def handle(self, notification: UserCreated) -> None:
        auth_user_id = await self._idp.get_auth_user_id()
        if await self._gateway.is_exists(auth_user_id):
            raise AuthUserAlreadyExistsError(auth_user_id=auth_user_id)

        auth_user = AuthUser(
            auth_user_id=auth_user_id,
            user_id=notification.user_id,
        )
        self._uow.add(auth_user)
