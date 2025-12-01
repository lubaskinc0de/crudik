from dishka import Provider, Scope, from_context

from crudik.adapters.config_loader import Config
from crudik.adapters.db.config import DbConfig


class ConfigProvider(Provider):
    scope = Scope.APP
    configs = from_context(Config) + from_context(DbConfig)
