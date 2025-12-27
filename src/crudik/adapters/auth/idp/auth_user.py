from typing import override

import jwt
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
    access_token_header: str
    access_token_alg: str
    allow_unverified_email: bool


@adapter
class WebAuthUserIdProvider(AuthUserIdProvider):
    """Adapter that extracts authentication user ID from HTTP request headers."""

    http_request: Request
    config: WebAuthUserIdProviderConfig

    @override
    async def get_auth_user_id(self) -> AuthUserId:
        """Reads the auth user ID from the configured HTTP header, raises UnauthorizedError if header is missing."""
        if (user_id := self.http_request.headers.get(self.config.user_id_header)) is None:
            logger.debug("Request unauthorized due to missing user id header", header=self.config.user_id_header)
            msg = f"Missing {self.config.user_id_header} header"
            raise UnauthorizedError(
                message=msg,
                reason=UnauthorizedReason.MISSING_USER_ID,
                header=self.config.user_id_header,
            )

        if not self.config.allow_unverified_email:
            access_token = self.http_request.headers.get(self.config.access_token_header)
            if access_token is None:
                logger.debug(
                    "Request unauthorized due to missing access token header",
                    header=self.config.access_token_header,
                )
                msg = f"Missing {self.config.access_token_header} header"
                raise UnauthorizedError(
                    message=msg,
                    reason=UnauthorizedReason.MISSING_ACCESS_TOKEN,
                    header=self.config.access_token_header,
                )
            try:
                email_verified: bool = jwt.decode(
                    access_token,
                    options={"verify_signature": False, "verify_exp": True},
                    algorithms=[self.config.access_token_alg],
                )["email_verified"]
            except KeyError as e:
                logger.debug("Request unauthorized due to corrupted access token")
                raise UnauthorizedError(
                    message="Corrupted access token",
                    reason=UnauthorizedReason.CORRUPTED_ACCESS_TOKEN,
                ) from e

            logger.debug("Email verified status", status=email_verified)
            if not email_verified:
                raise UnauthorizedError(
                    message="Email is not verified",
                    reason=UnauthorizedReason.EMAIL_IS_NOT_VERIFIED,
                )

        return user_id
