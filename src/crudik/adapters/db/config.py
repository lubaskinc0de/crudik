from dataclasses import dataclass

from sqlalchemy import URL


@dataclass(slots=True, kw_only=True)
class DbConfig:
    """Database connection configuration parameters."""

    user: str
    password: str
    host: str
    port: int
    db_name: str

    @property
    def connection_url(self) -> URL:
        """Constructs and returns the SQLAlchemy asyncpg connection URL string for database connections."""
        user = self.user
        password = self.password
        host = self.host
        port = self.port
        db_name = self.db_name

        return URL.create(
            drivername="postgresql+asyncpg",
            username=user,
            password=password,
            port=port,
            host=host,
            database=db_name,
        )
