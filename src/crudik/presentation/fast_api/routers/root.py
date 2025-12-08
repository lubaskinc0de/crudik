import structlog
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.common.logger import Logger

logger: Logger = structlog.get_logger(__name__)
router = APIRouter(
    tags=["Root"],
    route_class=DishkaRoute,
)


@router.get("/internal/alive")
async def alive() -> Response:
    """HTTP endpoint for liveness probe."""
    return Response(status_code=200)


@router.get("/internal/ready")
async def ready(
    session: FromDishka[AsyncSession],
) -> Response:
    """HTTP endpoint for readiness probe."""
    try:
        await session.execute(text("SELECT 1"))
    except Exception as e:  # noqa: BLE001
        await logger.awarning("Database is not ready", exc_info=e)
        return Response(status_code=429)

    return Response(status_code=200)
