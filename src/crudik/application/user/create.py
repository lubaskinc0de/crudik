from uuid import uuid4

from bazario.asyncio import Publisher
from pydantic import BaseModel

from crudik.application.common.event.user import UserCreated
from crudik.application.common.interactor import interactor
from crudik.application.common.uow import UoW
from crudik.entities.identifiers import UserId
from crudik.entities.user import User


class CreateUserOutput(BaseModel):
    id: UserId


@interactor
class CreateUser:
    publisher: Publisher
    uow: UoW

    async def execute(self) -> CreateUserOutput:
        user_id = uuid4()
        user = User(user_id)

        self.uow.add(user)
        await self.publisher.publish(UserCreated(user_id))
        await self.uow.commit()

        return CreateUserOutput(
            id=user_id,
        )
