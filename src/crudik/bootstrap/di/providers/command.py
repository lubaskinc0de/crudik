from dishka import Provider, Scope, provide_all

from crudik.application.example import ExampleCommand


class CommandProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ExampleCommand,
    )
