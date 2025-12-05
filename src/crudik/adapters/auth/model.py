from crudik.entities.base import model
from crudik.entities.common.identifiers import UserId
from crudik.entities.user import User

type AuthUserId = str


@model
class AuthUser:
    """Entity representing the link between an external authentication system user and an application user."""

    auth_user_id: AuthUserId
    user_id: UserId
    user: User
