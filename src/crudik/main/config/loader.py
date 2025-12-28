import os
from dataclasses import dataclass
from pathlib import Path

import toml_rs
from adaptix import Retort

from crudik.adapters.auth.idp.auth_user import WebAuthConfig
from crudik.adapters.db.config import DbConfig
from crudik.adapters.tracing import TracingConfig
from crudik.presentation.fast_api.config import ServerConfig

retort = Retort()


@dataclass(slots=True, kw_only=True)
class Config:
    """Main application configuration."""

    db: DbConfig
    web_auth: WebAuthConfig
    tracing: TracingConfig
    server: ServerConfig


def get_toml_config_path() -> Path:
    """Get TOML config path."""
    if (env_var := os.getenv("APP_CONFIG_PATH")) is None:
        msg = "Missing $APP_CONFIG_PATH"
        raise RuntimeError(msg)
    return Path(env_var)


def load_config_from_toml(toml_path: Path) -> Config:
    """Load ``Config`` from toml file."""
    file = toml_path.read_text("utf-8")
    return retort.load(toml_rs.loads(file, toml_version="1.1.0"), Config)
