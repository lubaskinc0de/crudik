from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from crudik.adapters.auth.idp.auth_user import WebAuthConfig
from crudik.adapters.db.config import DbConfig
from crudik.adapters.tracing import TracingConfig
from crudik.main.config.loader import Config
from crudik.main.di.providers.adapter import AdapterProvider
from crudik.main.di.providers.config import ConfigProvider
from crudik.main.di.providers.interactor import InteractorProvider
from crudik.main.di.providers.tracing import HTTPTracingProvider


def get_async_container(config: Config) -> AsyncContainer:
    """Creates and configures the async DI container with all providers and initial context values."""
    providers = [
        ConfigProvider(),
        FastapiProvider(),
        AdapterProvider(),
        InteractorProvider(),
        HTTPTracingProvider(),
    ]
    context = {
        Config: config,
        DbConfig: config.db,
        WebAuthConfig: config.web_auth,
        TracingConfig: config.tracing,
    }
    container = make_async_container(*providers, context=context, validation_settings=STRICT_VALIDATION)
    return container
