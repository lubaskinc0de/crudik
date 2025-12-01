from crudik.application.ping import Ping


async def test_ping() -> None:
    interactor = Ping()
    assert await interactor.execute() == "pong"
