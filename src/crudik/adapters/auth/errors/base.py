from enum import Enum
from typing import Any, ClassVar, override

from crudik.entities.errors.base import AppError, app_error


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
