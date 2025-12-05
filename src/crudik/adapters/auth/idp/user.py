from typing import override

from crudik.adapters.auth.common.gateway.auth_user import AuthUserGateway
from crudik.adapters.auth.errors.base import UnauthorizedError, UnauthorizedReason
from crudik.adapters.auth.idp.base import AuthUserIdProvider
from crudik.adapters.base import adapter
from crudik.application.common.idp import UserIdProvider
from crudik.entities.user import User


@adapter
class UserIdProviderImpl(UserIdProvider):
    """Adapter implementation that resolves application User entity from authentication user ID."""

    auth_user_idp: AuthUserIdProvider
    auth_user_gateway: AuthUserGateway

    @override
    async def get_user(self) -> User:
        """Resolves the authenticated user by looking up the auth user ID.

        and returning the associated application user.
        """
        auth_user_id = await self.auth_user_idp.get_auth_user_id()
        if (auth_user := await self.auth_user_gateway.get(auth_user_id)) is None:
            raise UnauthorizedError(reason=UnauthorizedReason.INVALID_AUTH_USER_ID)

        return auth_user.user
