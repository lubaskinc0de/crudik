from abc import abstractmethod
from typing import Protocol

from crudik.adapters.auth.model import AuthUserId


class AuthUserIdProvider(Protocol):
    """Protocol for extracting authentication user identifier from the request context."""

    @abstractmethod
    async def get_auth_user_id(self) -> AuthUserId:
        """Extracts and returns the authentication user ID from the current request (e.g., from headers or tokens)."""
        raise NotImplementedError
