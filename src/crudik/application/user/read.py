from pydantic import BaseModel

from crudik.application.common.gateway.user import UserGateway
from crudik.application.common.idp import UserIdProvider
from crudik.application.common.interactor import interactor
from crudik.application.errors.user import UserNotFoundError
from crudik.entities.common.identifiers import UserId
from crudik.entities.errors.base import AccessDeniedError


class ReadUserOutput(BaseModel):
    """Response model containing user data retrieved from the system."""

    id: UserId


@interactor
class ReadUser:
    """Use case interactor for reading user data."""

    gateway: UserGateway
    idp: UserIdProvider

    async def execute(self, user_id: UserId) -> ReadUserOutput:
        """Retrieves user data by ID, verifies the user exists, and ensures the requester has access to the data."""
        current_user = await self.idp.get_user()
        if (user := await self.gateway.get(user_id)) is None:
            raise UserNotFoundError(user_id=user_id)

        if user.id != current_user.id:
            raise AccessDeniedError

        return ReadUserOutput(
            id=user.id,
        )
