from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Protocol, override
from uuid import uuid4

from fastapi.requests import Request

from crudik.entities.errors.base import AppError, app_error

type TraceId = str


@app_error
class MissingTraceIdError(AppError):
    """Error that is raised when trace id is required but cannot be extracted from request."""

    header: str
    message: str = "Missing trace id"
    code: ClassVar[str] = "MISSING_TRACE_ID"

    @property
    @override
    def meta(self) -> dict[str, Any]:
        return {
            "header": self.header,
        }


@dataclass(slots=True, kw_only=True)
class TracingConfig:
    """Tracing configuration."""

    trace_id_header: str
    trace_id_required: bool = False


class TraceProvider(Protocol):
    """``TraceId`` provider."""

    @abstractmethod
    def get_trace_id(self) -> TraceId:
        """Provide ``TraceId``."""


@dataclass(frozen=True, kw_only=True, slots=True)
class HTTPTraceProvider(TraceProvider):
    """Provide ``TraceId`` from HTTP request headers."""

    request: Request
    config: TracingConfig

    @override
    def get_trace_id(self) -> TraceId:
        trace_id = self.request.headers.get(self.config.trace_id_header)
        if trace_id is None and self.config.trace_id_required:
            raise MissingTraceIdError(header=self.config.trace_id_header)

        if trace_id is None:
            trace_id = uuid4().hex

        return trace_id
