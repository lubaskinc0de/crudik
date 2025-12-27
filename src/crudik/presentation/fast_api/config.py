from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class ServerConfig:
    """HTTP-server configuration."""

    server_port: int
    server_host: str
