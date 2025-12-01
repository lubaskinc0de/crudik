from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from crudik.adapters.config_loader import Config
from crudik.adapters.db.config import DbConfig
from crudik.bootstrap.di.providers.adapter import AdapterProvider
from crudik.bootstrap.di.providers.config import ConfigProvider
from crudik.bootstrap.di.providers.interactor import Interactor


def get_async_container(config: Config) -> AsyncContainer:
    providers = [
        ConfigProvider(),
        FastapiProvider(),
        AdapterProvider(),
        Interactor(),
    ]
    context = {
        Config: config,
        DbConfig: config.db,
    }
    container = make_async_container(*providers, context=context)
    return container
