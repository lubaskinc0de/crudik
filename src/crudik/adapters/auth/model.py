from crudik.entities.base import model
from crudik.entities.common.identifiers import UserId

type AuthUserId = str


@model
class AuthUser:
    auth_user_id: AuthUserId
    user_id: UserId
