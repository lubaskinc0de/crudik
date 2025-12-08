from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

router = APIRouter(
    tags=["Root"],
    route_class=DishkaRoute,
)


@router.get("/ping/")
async def ping() -> str:
    """HTTP endpoint for health check that returns 'pong'."""
    return "pong"
