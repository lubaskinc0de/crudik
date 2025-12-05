from crudik.entities.base import model
from crudik.entities.common.identifiers import UserId


@model
class User:
    """Domain entity representing a user in the application. Contains only business data, not authentication details."""

    id: UserId
