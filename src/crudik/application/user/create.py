from uuid import uuid4

import structlog
from bazario.asyncio import Publisher
from pydantic import BaseModel

from crudik.application.common.event.user import UserCreated
from crudik.application.common.interactor import interactor
from crudik.application.common.logger import Logger
from crudik.application.common.uow import UoW
from crudik.entities.common.identifiers import UserId
from crudik.entities.user import User

logger: Logger = structlog.get_logger(__name__)


class CreateUserOutput(BaseModel):
    """Response model containing the info about newly created user."""

    id: UserId


@interactor
class CreateUser:
    """Use case interactor for creating a new user entity, publishes the UserCreated event."""

    publisher: Publisher
    uow: UoW

    async def execute(self) -> CreateUserOutput:
        """Creates a new user with a generated ID, persists it, publishes UserCreated event, and returns the user ID."""
        user_id = uuid4()
        logger.debug("Generated new user id", user_id=user_id)
        user = User(user_id)

        self.uow.add(user)

        await self.uow.flush([user])
        logger.debug("Publishing user created event")
        await self.publisher.publish(UserCreated(user_id))
        await self.uow.commit()

        logger.info("User created", user=user)
        return CreateUserOutput(
            id=user_id,
        )
