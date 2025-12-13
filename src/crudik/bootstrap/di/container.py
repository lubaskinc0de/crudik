from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProviderConfig
from crudik.adapters.db.config import DbConfig
from crudik.bootstrap.config.loader import Config
from crudik.bootstrap.di.providers.adapter import AdapterProvider
from crudik.bootstrap.di.providers.config import ConfigProvider
from crudik.bootstrap.di.providers.interactor import InteractorProvider
from crudik.bootstrap.di.providers.tracing import HTTPTracingProvider


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
        WebAuthUserIdProviderConfig: config.web_auth_user_id_provider,
    }
    container = make_async_container(*providers, context=context, validation_settings=STRICT_VALIDATION)
    return container
