from abc import abstractmethod
from collections.abc import Sequence
from typing import Any, Protocol


class UoW(Protocol):
    """Unit of Work protocol for managing database transactions and entity persistence operations."""

    @abstractmethod
    async def commit(self) -> None:
        """Commits all pending changes in the current transaction to the database."""
        ...

    @abstractmethod
    def add(self, instance: object) -> None:
        """Registers a new entity instance to be persisted when the transaction is committed."""
        ...

    @abstractmethod
    async def delete(self, instance: object) -> None:
        """Marks an entity instance for deletion when the transaction is committed."""
        ...

    @abstractmethod
    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        """Flushes pending changes to the database without committing the transaction."""
        ...
