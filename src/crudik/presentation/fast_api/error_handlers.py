from typing import Any, ClassVar

import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from crudik.adapters.auth.errors.auth_user import AuthUserAlreadyExistsError
from crudik.adapters.auth.errors.base import UnauthorizedError
from crudik.application.common.logger import Logger
from crudik.application.errors.user import UserNotFoundError
from crudik.entities.errors.base import AccessDeniedError, AppError, app_error

logger: Logger = structlog.get_logger(__name__)


@app_error
class InternalServerError(AppError):
    """Generic error used as fallback when an unexpected exception occurs."""

    code: ClassVar[str] = "INTERNAL_SERVER_ERROR"
    message: str = "Internal Server Error"


class ErrorResponse(BaseModel):
    """Standard error response model returned to API clients."""

    code: str
    message: str
    meta: dict[str, Any] | None


error_to_http_status: dict[type[AppError], int] = {
    UnauthorizedError: 401,
    AuthUserAlreadyExistsError: 409,
    UserNotFoundError: 404,
    AccessDeniedError: 403,
}


async def get_app_error_response(
    err: AppError,
) -> JSONResponse:
    """Converts an AppError to an appropriate HTTP JSON response with status code mapping."""
    try:
        http_status = error_to_http_status[type(err)]
    except KeyError:
        await logger.acritical("AppError is missing status code mapping", error_type=err.__class__.__qualname__)
        http_status = 500

    error_response = ErrorResponse(
        code=err.code,
        message=err.message,
        meta=err.meta,
    ).model_dump(mode="json")

    await logger.aexception("Handled error", error_response=error_response)
    return JSONResponse(
        status_code=http_status,
        content=error_response,
    )


async def app_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    """FastAPI exception handler that converts AppError exceptions to JSON error responses."""
    app_error = exc if isinstance(exc, AppError) else None
    if app_error is None:
        await logger.acritical("Internal server error")
        app_error = InternalServerError()
    return await get_app_error_response(app_error)
