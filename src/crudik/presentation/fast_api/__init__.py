from fastapi import FastAPI

from crudik.presentation.fast_api.error_handlers import (
    app_error_handler,
)
from crudik.presentation.fast_api.routers.root import router as root_router
from crudik.presentation.fast_api.routers.user import router as users_router


def include_routers(app: FastAPI) -> None:
    """Registers all API routers with the FastAPI application."""
    app.include_router(root_router)
    app.include_router(users_router)


def include_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers for converting exceptions to HTTP error responses."""
    app.add_exception_handler(Exception, app_error_handler)


__all__ = [
    "include_exception_handlers",
    "include_routers",
]
