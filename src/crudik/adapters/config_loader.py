import os
from dataclasses import dataclass
from typing import Self

from adaptix import Retort
from adaptix.load_error import LoadError

from crudik.adapters.db.config import DbConfig

ENV_PREFIX = "APP"

env_retort = Retort(strict_coercion=False)


def env[T = str](name: str, tp: type[T] | None = None, env_prefix: str = ENV_PREFIX) -> T:
    variable_name = f"{env_prefix}_{name}"
    try:
        return env_retort.load(os.environ[variable_name], tp if tp is not None else str)  # type: ignore
    except KeyError as e:
        msg = f"Environment variable '{variable_name}' is not set."
        raise RuntimeError(msg) from e
    except LoadError as e:
        msg = f"Cannot load environment variable '{variable_name}'."
        raise RuntimeError(msg) from e


@dataclass(frozen=True, slots=True)
class Config:
    db: DbConfig

    @classmethod
    def from_env(cls: type[Self]) -> Self:
        db = DbConfig(
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
            host=env("DB_HOST"),
            port=env("DB_PORT", int),
            db_name=env("DB_NAME"),
        )
        return cls(
            db=db,
        )
