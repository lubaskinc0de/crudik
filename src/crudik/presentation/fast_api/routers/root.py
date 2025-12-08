import structlog
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.common.logger import Logger

logger: Logger = structlog.get_logger(__name__)
router = APIRouter(
    tags=["Root"],
    route_class=DishkaRoute,
)


@router.get("/internal/alive")
async def alive() -> JSONResponse:
    """HTTP endpoint for liveness probe."""
    return JSONResponse(status_code=200, content={})


@router.get("/internal/ready")
async def ready(
    session: FromDishka[AsyncSession],
) -> JSONResponse:
    """HTTP endpoint for readiness probe."""
    try:
        await session.execute(text("SELECT 1"))
    except Exception as e:  # noqa: BLE001
        await logger.awarning("Database is not ready", exc_info=e)
        return JSONResponse(status_code=429, content={})

    return JSONResponse(status_code=200, content={})
