from abc import abstractmethod
from typing import Protocol

from crudik.domain.identifiers import UserId
from crudik.domain.user import User


class UserGateway(Protocol):
    @abstractmethod
    async def get(self, user_id: UserId) -> User | None:
        raise NotImplementedError
