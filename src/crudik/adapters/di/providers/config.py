from dishka import BaseScope, Provider, Scope, from_context

from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProviderConfig
from crudik.adapters.config.loader import Config
from crudik.adapters.db.config import DbConfig


class ConfigProvider(Provider):
    scope: BaseScope | None = Scope.APP
    configs = from_context(Config) + from_context(DbConfig) + from_context(WebAuthUserIdProviderConfig)
