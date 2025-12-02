from typing import override

from fastapi import Request

from crudik.adapters.auth.idp.base import AuthUserIdProvider, UnauthorizedError, UnauthorizedReason
from crudik.adapters.auth.model import AuthUserId
from crudik.adapters.base import adapter
from crudik.entities import config


@config
class WebAuthUserIdProviderConfig:
    user_id_header: str


@adapter
class WebAuthUserIdProvider(AuthUserIdProvider):
    http_request: Request
    config: WebAuthUserIdProviderConfig

    @override
    async def get_auth_user_id(self) -> AuthUserId:
        if (user_id := self.http_request.headers.get(self.config.user_id_header)) is None:
            msg = f"Missing {self.config.user_id_header} header"
            raise UnauthorizedError(
                message=msg,
                reason=UnauthorizedReason.MISSING_HEADER,
                header=self.config.user_id_header,
            )
        return user_id
