from abc import abstractmethod
from typing import Protocol

from crudik.entities.user import User


class UserIdProvider(Protocol):
    """Protocol for retrieving the currently authenticated user from the context."""

    @abstractmethod
    async def get_user(self) -> User:
        """Returns the User entity representing the currently authenticated user making the request."""
        raise NotImplementedError
