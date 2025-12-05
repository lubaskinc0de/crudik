from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(kw_only_default=True, frozen_default=True)
def interactor[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """Decorator that transforms a class into an immutable interactor dataclass for use case execution."""
    return dataclass(slots=True, kw_only=True, frozen=True)(cls)
