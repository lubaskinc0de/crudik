from typing import override

import structlog

from crudik.adapters.auth.common.gateway.auth_user import AuthUserGateway
from crudik.adapters.auth.errors.auth_user import AuthUserAlreadyExistsError
from crudik.adapters.auth.idp.base import AuthUserIdProvider
from crudik.adapters.auth.model import AuthUser
from crudik.application.common.auth_provider import AuthProvider
from crudik.application.common.gateway.user import UserGateway
from crudik.application.common.logger import Logger
from crudik.application.common.uow import UoW
from crudik.entities.user import User

logger: Logger = structlog.get_logger(__name__)


class SimpleAuthProvider(AuthProvider):
    """Auth provider that simply creates an AuthUser record when a User entity is created."""

    def __init__(
        self,
        uow: UoW,
        idp: AuthUserIdProvider,
        auth_user_gateway: AuthUserGateway,
        user_gateway: UserGateway,
    ) -> None:
        self._uow = uow
        self._idp = idp
        self._auth_user_gateway = auth_user_gateway
        self._user_gateway = user_gateway

    @override
    async def setup_auth(self, user: User) -> None:
        """Create auth user record."""
        logger.debug("Creating AuthUser record", user_id=user.id)

        auth_user_id = await self._idp.get_auth_user_id()
        logger.debug("Auth user id", auth_user_id=auth_user_id)

        if await self._auth_user_gateway.is_exists(auth_user_id):
            logger.info("Auth user already exists", auth_user_id=auth_user_id)
            raise AuthUserAlreadyExistsError(auth_user_id=auth_user_id)

        auth_user = AuthUser(
            auth_user_id=auth_user_id,
            user_id=user.id,
            user=user,
        )
        self._uow.add(auth_user)

        logger.info("Successfully created AuthUser entry", auth_user_id=auth_user_id, user_id=user.id)
