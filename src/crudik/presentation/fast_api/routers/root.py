from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.ping import Ping

router = APIRouter(
    tags=["Root"],
    route_class=DishkaRoute,
)


@router.get("/ping/")
async def ping(command: FromDishka[Ping]) -> str:
    """HTTP endpoint for health check that returns 'pong'."""
    return await command.execute()
