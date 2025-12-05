from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform(kw_only_default=True)
def config[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """Decorator that transforms a class into a configuration dataclass with keyword-only arguments."""
    return dataclass(slots=True, kw_only=True)(cls)
