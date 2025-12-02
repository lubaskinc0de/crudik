from crudik.domain.base import model
from crudik.domain.identifiers import UserId

type AuthUserId = str


@model
class AuthUser:
    auth_user_id: AuthUserId
    user_id: UserId
