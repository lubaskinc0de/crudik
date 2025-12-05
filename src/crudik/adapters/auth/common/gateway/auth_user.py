from abc import abstractmethod
from typing import Protocol

from crudik.adapters.auth.model import AuthUser, AuthUserId


class AuthUserGateway(Protocol):
    @abstractmethod
    async def is_exists(self, auth_user_id: AuthUserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get(self, auth_user_id: AuthUserId) -> AuthUser | None:
        raise NotImplementedError
