from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from crudik.bootstrap.config.loader import Config
from crudik.bootstrap.di.container import get_async_container
from crudik.bootstrap.logs import configure_structlog
from crudik.presentation.fast_api import include_exception_handlers, include_routers

log_config = configure_structlog()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """FastAPI lifespan context manager that handles DI container lifecycle during application startup and shutdown."""
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance with routers, error handlers, and DI container."""
    app = FastAPI(
        lifespan=lifespan,
        root_path="/api",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    container = get_async_container(Config.load())

    setup_dishka(container=container, app=app)

    include_routers(app)
    include_exception_handlers(app)

    return app


def run_api() -> None:
    """Starts the FastAPI application server using uvicorn on the configured host and port."""
    bind = "0.0.0.0"
    uvicorn.run(
        create_app(),
        port=5000,
        host=bind,
        log_config=log_config,
    )


if __name__ == "__main__":
    run_api()
