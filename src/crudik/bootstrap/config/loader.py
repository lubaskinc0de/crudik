from pathlib import Path
from typing import Self

import toml_rs
from adaptix import Retort

from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProviderConfig
from crudik.adapters.db.config import DbConfig
from crudik.adapters.env_loader import env
from crudik.adapters.tracing import TracingConfig
from crudik.entities import config
from crudik.presentation.fast_api.config import ServerConfig

retort = Retort()


@config
class TomlConfig:
    """Configuration structure loaded from TOML file matching the file's schema."""

    auth: WebAuthUserIdProviderConfig
    tracing: TracingConfig


@config
class Config:
    """Main application configuration."""

    db: DbConfig
    web_auth_user_id_provider: WebAuthUserIdProviderConfig
    tracing: TracingConfig
    server: ServerConfig

    @classmethod
    def load(cls) -> Self:
        """Loads configuration."""
        config_path = env("CONFIG_PATH", Path)

        with config_path.open("rb") as f:
            toml_config = retort.load(toml_rs.load(f), TomlConfig)

        db = DbConfig.from_env()
        server = ServerConfig(
            server_port=env("SERVER_PORT", int),
            server_host=env("SERVER_HOST"),
        )
        return cls(
            db=db,
            web_auth_user_id_provider=toml_config.auth,
            tracing=toml_config.tracing,
            server=server,
        )
