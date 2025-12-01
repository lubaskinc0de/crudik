from crudik.domain import config


@config
class DbConfig:
    user: str
    password: str
    host: str
    port: int
    db_name: str

    @property
    def connection_url(self) -> str:
        user = self.user
        password = self.password
        host = self.host
        db_name = self.db_name

        return f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}"
