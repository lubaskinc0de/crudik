from dishka import BaseScope, Provider, Scope, provide_all

from crudik.application.ping import Ping
from crudik.application.user.create import CreateUser
from crudik.application.user.read import ReadUser


class InteractorProvider(Provider):
    """Dishka provider that registers all use case interactors for dependency injection."""

    scope: BaseScope | None = Scope.REQUEST

    interactors = provide_all(
        CreateUser,
        ReadUser,
        Ping,
    )
