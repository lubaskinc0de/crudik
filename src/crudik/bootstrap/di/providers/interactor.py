from dishka import BaseScope, Provider, Scope, provide_all

from crudik.application.ping import Ping
from crudik.application.user.create import CreateUser


class InteractorProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    interactors = provide_all(
        CreateUser,
        Ping,
    )
