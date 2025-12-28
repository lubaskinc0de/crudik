from tests.api_client import ApiClient


async def test_alive_probe(api_client: ApiClient) -> None:
    """Test liveness probe."""
    response = await api_client.liveness()

    response.assert_status(200).ensure_ok()


async def test_readiness_probe(api_client: ApiClient) -> None:
    """Test readiness probe."""
    response = await api_client.readiness()

    response.assert_status(200).ensure_ok()
