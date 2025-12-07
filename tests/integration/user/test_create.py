from crudik.adapters.api_client import APIClient
from tests.integration.user.utils import create_user


async def test_ok(api_client: APIClient) -> None:
    """Test successful user creation."""
    with api_client.authenticate(auth_user_id="1"):
        response = await api_client.create_user()

    response.assert_status(200).ensure_ok()


async def test_already_exists(api_client: APIClient) -> None:
    """Test that creating a user with existing auth_user_id returns 409 error."""
    auth_user_id = "1"

    with api_client.authenticate(auth_user_id=auth_user_id):
        await create_user(api_client)
        response = await api_client.create_user()

    error = response.assert_status(409).ensure_err()
    assert error.code == "AUTH_USER_ALREADY_EXISTS"
    assert error.meta is not None
    assert "auth_user_id" in error.meta
    assert error.meta["auth_user_id"] == auth_user_id


async def test_unauthorized(api_client: APIClient) -> None:
    """Test that creating a user without authentication returns 401 error."""
    response = await api_client.create_user()

    error = response.assert_status(401).ensure_err()
    assert error.code == "UNAUTHORIZED"
