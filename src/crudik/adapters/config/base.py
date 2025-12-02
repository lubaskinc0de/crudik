import os

from adaptix import Retort
from adaptix.load_error import LoadError

ENV_PREFIX = "APP"

env_retort = Retort(strict_coercion=False)


def env[T = str](name: str, tp: type[T] | None = None, env_prefix: str = ENV_PREFIX) -> T:
    variable_name = f"{env_prefix}_{name}"
    try:
        return env_retort.load(os.environ[variable_name], tp if tp is not None else str)  # type: ignore[return-value]
    except KeyError as e:
        msg = f"Environment variable '{variable_name}' is not set."
        raise RuntimeError(msg) from e
    except LoadError as e:
        msg = f"Cannot load environment variable '{variable_name}'."
        raise RuntimeError(msg) from e
