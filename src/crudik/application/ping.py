from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Ping:
    """Simple health check interactor for verifying application availability."""

    async def execute(self) -> str:
        """Executes the health check and returns 'pong' to indicate the service is responding."""
        return "pong"
