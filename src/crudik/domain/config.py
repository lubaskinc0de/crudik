from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(kw_only_default=True)
def config[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """A decorator function that is used to standardize the creation of configuration classes."""
    return dataclass(slots=True, kw_only=True)(cls)
