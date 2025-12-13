from typing import Any, ClassVar

from pydantic import BaseModel

from crudik.entities.errors.base import AppError, app_error


class ErrorResponse(BaseModel):
    """Standard error response model returned to API clients."""

    code: str
    message: str
    meta: dict[str, Any] | None


@app_error
class InternalServerError(AppError):
    """Generic error used as fallback when an unexpected exception occurs."""

    code: ClassVar[str] = "INTERNAL_SERVER_ERROR"
    message: str = "Internal Server Error"
    orig_error: Exception
