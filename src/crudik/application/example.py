from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ExampleCommand:
    """Application business logic."""

    async def execute(self) -> str:
        """Read from gateway / write etc."""
        return "pong"
