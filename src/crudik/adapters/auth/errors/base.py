from enum import Enum
from typing import Any, ClassVar, override

from crudik.entities.errors.base import AppError, app_error


class UnauthorizedReason(Enum):
    """Enumeration of reasons why an authentication request may be unauthorized."""

    MISSING_USER_ID = "MISSING_USER_ID"
    INVALID_AUTH_USER_ID = "INVALID_AUTH_USER_ID"
    MISSING_ACCESS_TOKEN = "MISSING_ACCESS_TOKEN"  # noqa: S105
    CORRUPTED_ACCESS_TOKEN = "CORRUPTED_ACCESS_TOKEN"  # noqa: S105
    EMAIL_IS_NOT_VERIFIED = "EMAIL_IS_NOT_VERIFIED"


@app_error
class UnauthorizedError(AppError):
    """Error raised when a request cannot be authenticated or the authentication is invalid."""

    code: ClassVar[str] = "UNAUTHORIZED"
    reason: UnauthorizedReason
    header: str | None = None
    message: str = "Unauthorized"

    @property
    @override
    def meta(self) -> dict[str, Any] | None:
        return {
            "reason": self.reason,
            "header": self.header,
        }
