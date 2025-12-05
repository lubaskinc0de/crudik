from typing import Any, override

from bazario.asyncio import NotificationHandler

from crudik.adapters.auth.common.gateway.auth_user import AuthUserGateway
from crudik.adapters.auth.errors.auth_user import AuthUserAlreadyExistsError
from crudik.adapters.auth.idp.base import AuthUserIdProvider
from crudik.adapters.auth.model import AuthUser
from crudik.application.common.event.user import UserCreated
from crudik.application.common.gateway.user import UserGateway
from crudik.application.common.uow import UoW
from crudik.application.errors.user import UserNotFoundError


class UserCreatedHandler(NotificationHandler[UserCreated]):
    """Event handler that creates an AuthUser record when a User entity is created."""

    def __init__(
        self,
        *args: Any,
        uow: UoW,
        idp: AuthUserIdProvider,
        auth_user_gateway: AuthUserGateway,
        user_gateway: UserGateway,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._uow = uow
        self._idp = idp
        self._auth_user_gateway = auth_user_gateway
        self._user_gateway = user_gateway

    @override
    async def handle(self, notification: UserCreated) -> None:
        """Handles UserCreated event by linking the new user with the current authentication user ID."""
        auth_user_id = await self._idp.get_auth_user_id()
        if await self._auth_user_gateway.is_exists(auth_user_id):
            raise AuthUserAlreadyExistsError(auth_user_id=auth_user_id)

        if (user := await self._user_gateway.get(notification.user_id)) is None:
            # unreachable
            raise UserNotFoundError(user_id=notification.user_id)

        auth_user = AuthUser(
            auth_user_id=auth_user_id,
            user_id=user.id,
            user=user,
        )
        self._uow.add(auth_user)
