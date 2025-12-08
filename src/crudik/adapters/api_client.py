from dataclasses import dataclass
from typing import Self

from adaptix import Retort
from adaptix.load_error import LoadError
from aiohttp import ClientResponse, ClientResponseError, ClientSession

from crudik.adapters.auth.model import AuthUserId
from crudik.adapters.errors.http.response import ErrorResponse
from crudik.application.user.create import CreatedUser
from crudik.application.user.read import UserModel
from crudik.entities.common.config import config
from crudik.entities.common.identifiers import UserId

retort = Retort()


@dataclass
class EmptyResponse:
    """Empty response."""


@dataclass(slots=True, frozen=True)
class APIResponse[T]:
    """Response from API."""

    content: T | None
    http_response: ClientResponse
    status: int
    error: ErrorResponse | None = None

    def ensure_err(self) -> ErrorResponse:
        """Unwrap error response or raise ValueError if there is no error."""
        if self.error is None:
            msg = f"Cannot unwrap error, content = {self.content}"
            raise ValueError(msg)
        return self.error

    def ensure_ok(self) -> T:
        """Unwrap successful response or raise ValueError if error occurred."""
        if self.content is None:
            msg = f"Cannot unwrap response, status = {self.status}, error = {self.error}"
            raise ValueError(msg)
        return self.content

    def assert_status(self, status: int) -> Self:
        """Assert that response status matches expected value."""
        if self.status != status:
            msg = f"HTTP status assertion failed. {self.status} != {status}"
            raise ValueError(msg)
        return self


@config
class APIClientConfig:
    """Config for APIClient."""

    auth_user_id_header: str


class AuthContext:
    """Context manager for setting authentication."""

    def __init__(self, api_client: "APIClient", auth_user_id: AuthUserId, config: APIClientConfig) -> None:
        self._api_client = api_client
        self._auth_user_id = auth_user_id
        self._config = config

    def __enter__(self) -> None:
        """Set authentication header for the duration of the context."""
        self._api_client.set_header(self._config.auth_user_id_header, self._auth_user_id)

    def __exit__(self, *exc_info: object) -> None:
        """Remove authentication header after the context."""
        self._api_client.remove_header(self._config.auth_user_id_header)
        if exc_info[0] is not None:  # exc type
            raise exc_info[1]  # type: ignore[misc] # exc value


class APIClient:
    """Client for making API requests."""

    def __init__(self, session: ClientSession, config: APIClientConfig) -> None:
        self.session = session
        self._headers: dict[str, str] = {}
        self._config = config

    async def _load_response[T](self, response: ClientResponse, response_type: type[T] | None) -> APIResponse[T]:
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

    def set_header(self, header: str, value: str) -> None:
        """Add HTTP header."""
        self._headers[header] = value

    def remove_header(self, header: str) -> None:
        """Remove HTTP header."""
        del self._headers[header]

    def authenticate(self, *, auth_user_id: AuthUserId) -> AuthContext:
        """Set auth user ID for requests."""
        return AuthContext(self, auth_user_id, self._config)

    async def readiness(self) -> APIResponse[EmptyResponse]:
        """GET /internal/ready."""
        url = "/internal/ready"
        async with self.session.get(url, headers=self._headers) as response:
            return await self._load_response(
                response,
                response_type=EmptyResponse,
            )

    async def liveness(self) -> APIResponse[EmptyResponse]:
        """GET /internal/alive."""
        url = "/internal/alive"
        async with self.session.get(url, headers=self._headers) as response:
            return await self._load_response(
                response,
                response_type=EmptyResponse,
            )

    async def create_user(self) -> APIResponse[CreatedUser]:
        """Create a new user via POST /users/."""
        url = "/users/"
        async with self.session.post(url, headers=self._headers) as response:
            return await self._load_response(
                response,
                response_type=CreatedUser,
            )

    async def read_user(self, user_id: UserId) -> APIResponse[UserModel]:
        """Read user by id via GET /users/{user_id}."""
        url = f"/users/{user_id}"
        async with self.session.get(url, headers=self._headers) as response:
            return await self._load_response(
                response,
                response_type=UserModel,
            )
