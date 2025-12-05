from tests.integration.api_client import APIClient


async def test_ok(client: APIClient) -> None:
    client.set_auth_user_id("1")

    (await client.create_user()).assert_status(200).unwrap()


async def test_already_exists(client: APIClient) -> None:
    client.set_auth_user_id("1")
    (await client.create_user()).assert_status(200).unwrap()

    error = (await client.create_user()).assert_status(409).unwrap_err()

    assert error.code == "AUTH_USER_ALREADY_EXISTS"
    assert error.meta is not None
    assert "auth_user_id" in error.meta
    assert error.meta["auth_user_id"] == "1"
