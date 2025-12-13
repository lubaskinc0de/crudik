from collections.abc import Awaitable, Callable

import structlog
from dishka import AsyncContainer
from fastapi import Request, Response

from crudik.adapters.tracing import TraceId


async def tracing_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Middleware that binds trace id logging contextvar for each request."""
    if request.method not in {"GET", "POST", "DELETE", "PUT", "PATCH"}:
        return await call_next(request)

    dishka_container: AsyncContainer = request.state.dishka_container
    trace_id: TraceId = await dishka_container.get(TraceId)
    with structlog.contextvars.bound_contextvars(trace_id=trace_id):
        return await call_next(request)
