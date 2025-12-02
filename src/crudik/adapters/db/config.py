from typing import Self

from crudik.adapters.config.base import env
from crudik.entities import config


@config
class DbConfig:
    user: str
    password: str
    host: str
    port: int
    db_name: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
            host=env("DB_HOST"),
            port=env("DB_PORT", int),
            db_name=env("DB_NAME"),
        )

    @property
    def connection_url(self) -> str:
        user = self.user
        password = self.password
        host = self.host
        db_name = self.db_name

        return f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}"
