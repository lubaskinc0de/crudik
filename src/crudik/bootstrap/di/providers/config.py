from dishka import BaseScope, Provider, Scope, from_context

from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProviderConfig
from crudik.adapters.db.config import DbConfig
from crudik.adapters.tracing import TracingConfig
from crudik.bootstrap.config.loader import Config


class ConfigProvider(Provider):
    """Dishka provider that exposes configuration objects from the context."""

    scope: BaseScope | None = Scope.APP
    configs = (
        from_context(Config)
        + from_context(DbConfig)
        + from_context(WebAuthUserIdProviderConfig)
        + from_context(TracingConfig)
    )
