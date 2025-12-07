from typing import override

import structlog
from fastapi import Request

from crudik.adapters.auth.errors.base import UnauthorizedError, UnauthorizedReason
from crudik.adapters.auth.idp.base import AuthUserIdProvider
from crudik.adapters.auth.model import AuthUserId
from crudik.adapters.base import adapter
from crudik.application.common.logger import Logger
from crudik.entities import config

logger: Logger = structlog.get_logger(__name__)


@config
class WebAuthUserIdProviderConfig:
    """Configuration for web-based authentication user ID provider."""

    user_id_header: str


@adapter
class WebAuthUserIdProvider(AuthUserIdProvider):
    """Adapter that extracts authentication user ID from HTTP request headers."""

    http_request: Request
    config: WebAuthUserIdProviderConfig

    @override
    async def get_auth_user_id(self) -> AuthUserId:
        """Reads the auth user ID from the configured HTTP header, raises UnauthorizedError if header is missing."""
        if (user_id := self.http_request.headers.get(self.config.user_id_header)) is None:
            await logger.adebug("Request unauthorized due to missing header", header=self.config.user_id_header)
            msg = f"Missing {self.config.user_id_header} header"
            raise UnauthorizedError(
                message=msg,
                reason=UnauthorizedReason.MISSING_HEADER,
                header=self.config.user_id_header,
            )
        return user_id
