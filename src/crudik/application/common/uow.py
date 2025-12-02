from abc import abstractmethod
from collections.abc import Sequence
from typing import Any, Protocol


class UoW(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    def add(self, instance: object) -> None: ...

    @abstractmethod
    async def delete(self, instance: object) -> None: ...

    @abstractmethod
    async def flush(self, objects: Sequence[Any] | None = None) -> None: ...
