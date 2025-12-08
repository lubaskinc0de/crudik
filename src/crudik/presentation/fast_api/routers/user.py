from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.user.create import CreatedUser, CreateUser
from crudik.application.user.read import ReadUser, UserModel
from crudik.entities.common.identifiers import UserId

router = APIRouter(
    tags=["Users"],
    route_class=DishkaRoute,
    prefix="/users",
)


@router.post("/")
async def create(
    interactor: FromDishka[CreateUser],
) -> CreatedUser:
    """HTTP endpoint for creating a new user."""
    return await interactor.execute()


@router.get("/{user_id}")
async def read(
    interactor: FromDishka[ReadUser],
    user_id: UserId,
) -> UserModel:
    """HTTP endpoint for retrieving user data by ID."""
    return await interactor.execute(user_id)
