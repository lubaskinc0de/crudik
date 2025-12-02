from abc import abstractmethod
from enum import Enum
from typing import Any, ClassVar, Protocol, override

from crudik.adapters.auth.model import AuthUserId
from crudik.entities.errors.base import AppError, app_error


class AuthUserIdProvider(Protocol):
    @abstractmethod
    async def get_auth_user_id(self) -> AuthUserId:
        raise NotImplementedError


class UnauthorizedReason(Enum):
    MISSING_HEADER = "MISSING_HEADER"


@app_error
class UnauthorizedError(AppError):
    code: ClassVar[str] = "UNAUTHORIZED"
    reason: UnauthorizedReason
    header: str | None = None

    @property
    @override
    def meta(self) -> dict[str, Any] | None:
        return {
            "reason": self.reason,
            "header": self.header,
        }
