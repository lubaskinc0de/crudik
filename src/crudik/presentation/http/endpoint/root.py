from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.example import ExampleCommand

router = APIRouter(
    tags=["Root"],
    route_class=DishkaRoute,
)


@router.get("/ping/")
async def ping(command: FromDishka[ExampleCommand]) -> str:
    return await command.execute()
