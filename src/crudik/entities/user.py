from dataclasses import dataclass

from crudik.entities.common.identifiers import UserId


@dataclass
class User:
    """Domain entity representing a user in the application. Contains only business data, not authentication details."""

    id: UserId
