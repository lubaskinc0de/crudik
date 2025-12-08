from uuid import uuid4

import structlog
from pydantic import BaseModel

from crudik.application.common.auth_provider import AuthProvider
from crudik.application.common.interactor import interactor
from crudik.application.common.logger import Logger
from crudik.application.common.uow import UoW
from crudik.entities.common.identifiers import UserId
from crudik.entities.user import User

logger: Logger = structlog.get_logger(__name__)


class CreatedUser(BaseModel):
    """Response model containing the info about newly created user."""

    id: UserId


@interactor
class CreateUser:
    """Interactor for creating a new user entity."""

    uow: UoW
    auth_provider: AuthProvider

    async def execute(self) -> CreatedUser:
        """Creates a new user with a generated ID."""
        logger.debug("Creating new user")
        user_id = uuid4()
        logger.debug("Generated new user id", user_id=user_id)
        user = User(user_id)

        self.uow.add(user)
        await self.uow.flush([user])
        await self.auth_provider.setup_auth(user)
        await self.uow.commit()

        logger.info("User created", user=user)
        return CreatedUser(
            id=user_id,
        )
