from crudik.entities.common.config import config


@config
class ServerConfig:
    """HTTP-server configuration."""

    server_port: int
    server_host: str
