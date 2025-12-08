import structlog
from pydantic import BaseModel

from crudik.application.common.gateway.user import UserGateway
from crudik.application.common.idp import UserIdProvider
from crudik.application.common.interactor import interactor
from crudik.application.common.logger import Logger
from crudik.application.errors.user import UserNotFoundError
from crudik.entities.common.identifiers import UserId
from crudik.entities.errors.base import AccessDeniedError

logger: Logger = structlog.get_logger(__name__)


class UserModel(BaseModel):
    """Response model containing user data retrieved from the system."""

    id: UserId


@interactor
class ReadUser:
    """Use case interactor for reading user data."""

    gateway: UserGateway
    idp: UserIdProvider

    async def execute(self, user_id: UserId) -> UserModel:
        """Retrieves user data by ID, verifies the user exists, and ensures the requester has access to the data."""
        logger.debug("Read user request", user_id=user_id)
        current_user = await self.idp.get_user()
        logger.debug("Current user id", user_id=current_user.id)

        if (user := await self.gateway.get(user_id)) is None:
            logger.debug("User by id not found", user_id=user_id)
            raise UserNotFoundError(user_id=user_id)

        if user.id != current_user.id:
            logger.debug("Read user access denied", current_user_id=current_user.id, user_id=user_id)
            raise AccessDeniedError

        logger.info("Read user successfull", user_id=user_id)
        return UserModel(
            id=user.id,
        )
