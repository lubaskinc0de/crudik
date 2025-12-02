from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(kw_only_default=True, frozen_default=True)
def adapter[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """A decorator function that is used to standardize the creation of adapters dataclasses."""
    return dataclass(cls, frozen=True, kw_only=True, slots=True)
