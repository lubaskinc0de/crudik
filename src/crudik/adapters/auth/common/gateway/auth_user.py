from abc import abstractmethod
from typing import Protocol

from crudik.adapters.auth.model import AuthUser, AuthUserId


class AuthUserGateway(Protocol):
    """Protocol defining the interface for accessing authentication user records from persistent storage."""

    @abstractmethod
    async def is_exists(self, auth_user_id: AuthUserId) -> bool:
        """Checks whether an authentication user record exists for the given auth user ID."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, auth_user_id: AuthUserId) -> AuthUser | None:
        """Retrieves an authentication user entity by ID, returns None if not found."""
        raise NotImplementedError
