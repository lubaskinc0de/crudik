from dataclasses import dataclass
from typing import Self, TypeVar

from adaptix import Retort
from adaptix.load_error import LoadError
from aiohttp import ClientResponse, ClientResponseError, ClientSession

from crudik.adapters.auth.model import AuthUserId
from crudik.application.user.create import CreateUserOutput
from crudik.application.user.read import ReadUserOutput
from crudik.entities.common.identifiers import UserId
from crudik.presentation.fast_api.error_handlers import ErrorResponse

retort = Retort()
T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class APIResponse[T]:
    """Wrapper for API response with content, status and error handling."""

    content: T | None
    http_response: ClientResponse
    status: int
    error: ErrorResponse | None = None

    def unwrap_err(self) -> ErrorResponse:
        """Unwrap error response or raise ValueError if no error."""
        if self.error is None:
            msg = f"Cannot unwrap error, content = {self.content}"
            raise ValueError(msg)
        return self.error

    def unwrap(self) -> T:
        """Unwrap successful response or raise ValueError if error occurred."""
        if self.content is None:
            msg = f"Cannot unwrap response, status = {self.status}, error = {self.error}"
            raise ValueError(msg)
        return self.content

    def assert_status(self, status: int) -> Self:
        """Assert that response status matches expected value."""
        assert self.status == status
        return self


class APIClient:
    """Client for making API requests."""

    def __init__(self, session: ClientSession) -> None:
        self.session = session
        self._headers: dict[str, str] = {}

    def set_headers(self, headers: dict[str, str]) -> None:
        """Set custom HTTP headers for requests."""
        self._headers = headers

    def set_auth_user_id(self, auth_user_id: AuthUserId) -> None:
        """Set authentication user ID in headers."""
        self._headers["X-Auth-User"] = auth_user_id

    def reset_auth_user_id(self) -> None:
        """Remove authentication user ID from headers."""
        del self._headers["X-Auth-User"]

    async def _load_response[T](self, response: ClientResponse, response_type: type[T]) -> APIResponse[T]:
        """Load response content or error from HTTP response."""
        try:
            response.raise_for_status()
        except ClientResponseError as response_error:
            try:
                return APIResponse(
                    content=None,
                    error=retort.load(await response.json(), ErrorResponse),
                    status=response.status,
                    http_response=response,
                )
            except LoadError as load_error:
                raise load_error from response_error
        else:
            return APIResponse(
                content=retort.load(await response.json(), response_type),
                http_response=response,
                status=response.status,
            )

    async def create_user(self) -> APIResponse[CreateUserOutput]:
        """Create a new user via POST /users/."""
        url = "/users/"
        async with self.session.post(url, headers=self._headers) as response:
            return await self._load_response(
                response,
                response_type=CreateUserOutput,
            )

    async def read_user(self, user_id: UserId) -> APIResponse[ReadUserOutput]:
        """Read user by id via GET /users/{user_id}."""
        url = f"/users/{user_id}"
        async with self.session.get(url, headers=self._headers) as response:
            return await self._load_response(
                response,
                response_type=ReadUserOutput,
            )
