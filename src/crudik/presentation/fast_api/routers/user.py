from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.user.create import CreateUser, CreateUserOutput

router = APIRouter(
    tags=["Users"],
    route_class=DishkaRoute,
    prefix="/users",
)


@router.post("/")
async def create_user(
    command: FromDishka[CreateUser],
) -> CreateUserOutput:
    return await command.execute()
