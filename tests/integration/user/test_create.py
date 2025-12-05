from tests.integration.api_client import APIClient
from tests.integration.user.utils import create_user


async def test_ok(client: APIClient) -> None:
    client.set_auth_user_id("1")

    (await client.create_user()).assert_status(200).unwrap()


async def test_already_exists(client: APIClient) -> None:
    auth_user_id = "1"
    await create_user(client, auth_user_id)
    client.set_auth_user_id(auth_user_id)

    error = (await client.create_user()).assert_status(409).unwrap_err()

    assert error.code == "AUTH_USER_ALREADY_EXISTS"
    assert error.meta is not None
    assert "auth_user_id" in error.meta
    assert error.meta["auth_user_id"] == auth_user_id


async def test_unauthorized(client: APIClient) -> None:
    error = (await client.create_user()).assert_status(401).unwrap_err()

    assert error.code == "UNAUTHORIZED"
