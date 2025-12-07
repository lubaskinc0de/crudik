from pathlib import Path
from typing import Self

import toml_rs
from adaptix import Retort

from crudik.adapters.auth.idp.auth_user import WebAuthUserIdProviderConfig
from crudik.adapters.config.base import env
from crudik.adapters.db.config import DbConfig
from crudik.entities import config

retort = Retort()


@config
class TomlConfig:
    """Configuration structure loaded from TOML file matching the file's schema."""

    auth: WebAuthUserIdProviderConfig


@config
class Config:
    """Main application configuration."""

    db: DbConfig
    web_auth_user_id_provider: WebAuthUserIdProviderConfig

    @classmethod
    def load(cls) -> Self:
        """Loads configuration."""
        config_path = env("CONFIG_PATH", Path)

        with config_path.open("rb") as f:
            toml_config = retort.load(toml_rs.load(f), TomlConfig)

        db = DbConfig.from_env()
        return cls(
            db=db,
            web_auth_user_id_provider=toml_config.auth,
        )
