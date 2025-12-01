from crudik.domain.base import entity
from crudik.domain.identifiers import UserId


@entity
class User:
    """A class that represents the entity of the user of the application.

    This entity contains the user business data required by the application.
    This entity should not contain any authentication information (unless the domain requires it)
    as it applies to adapters.
    """

    id: UserId
