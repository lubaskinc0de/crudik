from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class ServerConfig:
    """HTTP-server configuration."""

    port: int
    host: str
