from abc import abstractmethod
from typing import Protocol

from crudik.entities.user import User


class AuthProvider(Protocol):
    """External auth system."""

    @abstractmethod
    async def setup_auth(self, user: User) -> None:
        """Binds the user that is created to the authentication system."""
        raise NotImplementedError
