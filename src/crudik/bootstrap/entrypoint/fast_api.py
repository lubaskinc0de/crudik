from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from crudik.adapters.config.loader import Config
from crudik.bootstrap.di.container import get_async_container
from crudik.presentation.fast_api import include_exception_handlers, include_routers

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
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
    bind = "0.0.0.0"
    uvicorn.run(
        create_app(),
        port=5000,
        host=bind,
        log_config=log_config,
    )


if __name__ == "__main__":
    run_api()
