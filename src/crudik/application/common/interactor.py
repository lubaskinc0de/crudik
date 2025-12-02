from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(kw_only_default=True, frozen_default=True)
def interactor[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """A decorator function that is used to standardize the creation of interactors."""
    return dataclass(slots=True, kw_only=True, frozen=True)(cls)
