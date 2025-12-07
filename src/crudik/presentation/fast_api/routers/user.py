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
    interactor: FromDishka[CreateUser],
) -> CreateUserOutput:
    """HTTP endpoint for creating a new user."""
    return await interactor.execute()


@router.get("/{user_id}")
async def read_user(
    interactor: FromDishka[ReadUser],
    user_id: UserId,
) -> ReadUserOutput:
    """HTTP endpoint for retrieving user data by ID."""
    return await interactor.execute(user_id)
