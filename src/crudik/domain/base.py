from abc import ABC
from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(kw_only_default=False)
def entity[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """A decorator function that is used to standardize the creation of dataclass entities."""
    return dataclass(cls)


@entity
class Entity(ABC):  # noqa: B024
    """A base abstract class for all entities.

    Usually does not contain a common behavior and/or fields.
    """
