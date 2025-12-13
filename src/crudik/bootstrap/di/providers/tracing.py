from dishka import BaseScope, Provider, Scope, WithParents, from_context, provide
from fastapi import Request

from crudik.adapters.tracing import HTTPTraceProvider, TraceId


class HTTPTracingProvider(Provider):
    """Dishka provider that provides tracing functional for HTTP application."""

    scope: BaseScope | None = Scope.REQUEST
    request = from_context(Request)
    trace_provider = provide(WithParents[HTTPTraceProvider])

    @provide
    def provide_trace_id(self, trace_provider: HTTPTraceProvider) -> TraceId:
        """Provide trace id."""
        return trace_provider.get_trace_id()
