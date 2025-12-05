from abc import ABC
from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(kw_only_default=False)
def model[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """Decorator that transforms a class into a dataclass for domain entity modeling."""
    return dataclass(cls)


@model
class Entity(ABC):  # noqa: B024
    """Base abstract class that all domain entities inherit from. Provides common structure for business objects."""
