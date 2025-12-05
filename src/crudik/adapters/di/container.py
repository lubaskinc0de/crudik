from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProviderConfig
from crudik.adapters.config.loader import Config
from crudik.adapters.db.config import DbConfig
from crudik.adapters.di.providers.adapter import AdapterProvider
from crudik.adapters.di.providers.config import ConfigProvider
from crudik.adapters.di.providers.interactor import InteractorProvider


def get_async_container(config: Config) -> AsyncContainer:
    providers = [
        ConfigProvider(),
        FastapiProvider(),
        AdapterProvider(),
        InteractorProvider(),
    ]
    context = {
        Config: config,
        DbConfig: config.db,
        WebAuthUserIdProviderConfig: config.web_auth_user_id_provider,
    }
    container = make_async_container(*providers, context=context, validation_settings=STRICT_VALIDATION)
    return container
