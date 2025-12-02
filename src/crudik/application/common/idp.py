from abc import abstractmethod
from typing import Protocol

from crudik.domain.user import User


class UserIdProvider(Protocol):
    @abstractmethod
    async def get_user(self) -> User:
        raise NotImplementedError
