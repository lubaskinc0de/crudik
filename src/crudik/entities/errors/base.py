from dataclasses import dataclass
from typing import Any, ClassVar, dataclass_transform, override


@dataclass_transform(kw_only_default=True)
def app_error[ClsT](cls: type[ClsT]) -> type[ClsT]:
    """A decorator function that is used to standardize the creation of application errors."""
    return dataclass(slots=True, kw_only=True)(cls)


@app_error
class AppError(Exception):
    """A base abstract class for all application (business) errors.

    This class serves as the foundation for all domain-specific exceptions
    in the application. It provides a structured way to handle business logic
    errors with consistent error codes, messages, and optional metadata.

    Attributes:
        message (str): Human-readable error description.
        code (ClassVar[str]): Unique error code identifier (class-level attribute).

    Properties:
        meta: Optional dictionary containing additional error context.

    Notes:
        - Subclasses must define the `code` class variable.
        - The `message` can be overridden via instance initialization.
        - The `meta` property can be overridden to provide structured
          contextual information about the error.

    Example:
        ```python
        @app_error
        class UserNotFoundError(AppError):
            user_id: UUID
            code = "USER_NOT_FOUND"

            @property
            def meta(self):
                return {"user_id": self.user_id}
        ```

    """

    message: str
    code: ClassVar[str]

    @property
    def meta(self) -> dict[str, Any] | None:
        """Returns optional metadata associated with the error.

        This property can be overridden in subclasses to provide
        structured contextual information that might be useful for
        error handling, logging, or client responses.

        Returns:
            Optional dictionary containing error metadata, or None
            if no additional context is available.

        """
        return None

    @override
    def __str__(self) -> str:
        return f"{self.code}: {self.message}{'\n':<6}meta={self.meta}"


@app_error
class AccessDeniedError(AppError):
    code: ClassVar[str] = "ACCESS_DENIED"
    message: str = "Access denied"
