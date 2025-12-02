from abc import abstractmethod
from typing import Protocol

from crudik.entities.identifiers import UserId
from crudik.entities.user import User


class UserGateway(Protocol):
    @abstractmethod
    async def get(self, user_id: UserId) -> User | None:
        raise NotImplementedError
