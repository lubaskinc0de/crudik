from crudik.adapters.api_client import APIClient


async def test_alive(api_client: APIClient) -> None:
    """Test liveness probe."""
    response = await api_client.liveness()

    response.assert_status(200).ensure_ok()


async def test_readiness(api_client: APIClient) -> None:
    """Test readiness probe."""
    response = await api_client.readiness()

    response.assert_status(200).ensure_ok()
