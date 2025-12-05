from abc import abstractmethod
from typing import Protocol

from crudik.adapters.auth.model import AuthUserId


class AuthUserGateway(Protocol):
    @abstractmethod
    async def is_exists(self, auth_user_id: AuthUserId) -> bool:
        raise NotImplementedError
