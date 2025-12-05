from dataclasses import dataclass
from typing import Any, ClassVar, dataclass_transform, override


@dataclass_transform(kw_only_default=True)
def app_error[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """Decorator that transforms a class into a standardized application error dataclass."""
    return dataclass(slots=True, kw_only=True)(cls)


@app_error
class AppError(Exception):
    """Base exception class for all domain-level business logic errors in the application."""

    message: str
    code: ClassVar[str]

    @property
    def meta(self) -> dict[str, Any] | None:
        """Returns optional metadata dictionary with additional error context."""
        return None

    @override
    def __str__(self) -> str:
        return f"{self.code}: {self.message}{'\n':<6}meta={self.meta}"


@app_error
class AccessDeniedError(AppError):
    """Error raised when a user attempts to access a resource they don't have permission for."""

    code: ClassVar[str] = "ACCESS_DENIED"
    message: str = "Access denied"
