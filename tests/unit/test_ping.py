from crudik.application.ping import Ping


async def test_ping() -> None:
    """Test that ping returns 'pong'."""
    interactor = Ping()
    assert await interactor.execute() == "pong"
