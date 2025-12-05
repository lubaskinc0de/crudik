from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.user.create import CreateUser, CreateUserOutput
from crudik.application.user.read import ReadUser, ReadUserOutput
from crudik.entities.common.identifiers import UserId

router = APIRouter(
    tags=["Users"],
    route_class=DishkaRoute,
    prefix="/users",
)


@router.post("/")
async def create_user(
    command: FromDishka[CreateUser],
) -> CreateUserOutput:
    """HTTP endpoint for creating a new user."""
    return await command.execute()


@router.get("/{user_id}")
async def read_user(
    command: FromDishka[ReadUser],
    user_id: UserId,
) -> ReadUserOutput:
    """HTTP endpoint for retrieving user data by ID."""
    return await command.execute(user_id)
