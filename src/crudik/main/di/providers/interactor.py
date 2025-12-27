from dishka import BaseScope, Provider, Scope, provide_all

from crudik.application.create_user import CreateUser
from crudik.application.read_user import ReadUser


class InteractorProvider(Provider):
    """Dishka provider that registers all use case interactors for dependency injection."""

    scope: BaseScope | None = Scope.REQUEST

    interactors = provide_all(
        CreateUser,
        ReadUser,
    )
