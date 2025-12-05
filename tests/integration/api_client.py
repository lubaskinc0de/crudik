from dataclasses import dataclass
from typing import Self, TypeVar

from adaptix import Retort
from adaptix.load_error import LoadError
from aiohttp import ClientResponse, ClientResponseError, ClientSession

from crudik.adapters.auth.model import AuthUserId
from crudik.application.user.create import CreateUserOutput
from crudik.presentation.fast_api.error_handlers import ErrorResponse

retort = Retort()
T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class APIResponse[T]:
    content: T | None
    http_response: ClientResponse
    status: int
    error: ErrorResponse | None = None

    def unwrap_err(self) -> ErrorResponse:
        if self.error is None:
            msg = f"Cannot unwrap error, content = {self.content}"
            raise ValueError(msg)
        return self.error

    def unwrap(self) -> T:
        if self.content is None:
            msg = f"Cannot unwrap response, status = {self.status}, error = {self.error}"
            raise ValueError(msg)
        return self.content

    def assert_status(self, status: int) -> Self:
        assert self.status == status
        return self


class APIClient:
    def __init__(self, session: ClientSession) -> None:
        self.session = session
        self._headers: dict[str, str] = {}

    def set_headers(self, headers: dict[str, str]) -> None:
        self._headers = headers

    def set_auth_user_id(self, auth_user_id: AuthUserId) -> None:
        self._headers["X-Auth-User"] = auth_user_id

    async def _load_response[T](self, response: ClientResponse, response_type: type[T]) -> APIResponse[T]:
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
        url = "/users/"
        async with self.session.post(url, headers=self._headers) as response:
            return await self._load_response(
                response,
                response_type=CreateUserOutput,
            )
