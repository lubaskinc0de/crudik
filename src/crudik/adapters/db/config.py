from typing import Self

from crudik.adapters.env_loader import env
from crudik.entities import config


@config
class DbConfig:
    """Database connection configuration parameters."""

    user: str
    password: str
    host: str
    port: int
    db_name: str

    @classmethod
    def from_env(cls) -> Self:
        """Creates database configuration by reading connection parameters from environment variables."""
        return cls(
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
            host=env("DB_HOST"),
            port=env("DB_PORT", int),
            db_name=env("DB_NAME"),
        )

    @property
    def connection_url(self) -> str:
        """Constructs and returns the SQLAlchemy asyncpg connection URL string for database connections."""
        user = self.user
        password = self.password
        host = self.host
        db_name = self.db_name

        return f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}"
