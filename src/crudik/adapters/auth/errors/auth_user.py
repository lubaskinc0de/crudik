from typing import Any, ClassVar, override

from crudik.adapters.auth.model import AuthUserId
from crudik.entities.errors.base import AppError, app_error


@app_error
class AuthUserAlreadyExistsError(AppError):
    code: ClassVar[str] = "AUTH_USER_ALREADY_EXISTS"
    auth_user_id: AuthUserId
    message: str = "Auth user already exists"

    @property
    @override
    def meta(self) -> dict[str, Any] | None:
        return {
            "auth_user_id": self.auth_user_id,
        }
