from uuid import uuid4

from tests.integration.api_client import APIClient
from tests.integration.user.utils import create_user


async def test_ok(client: APIClient) -> None:
    """Test successful user read by id."""
    auth_user_id = "1"
    user_id = await create_user(client, auth_user_id)
    client.set_auth_user_id(auth_user_id)

    content = (await client.read_user(user_id)).assert_status(200).unwrap()

    assert content.id == user_id


async def test_not_exists(client: APIClient) -> None:
    """Test that reading non-existent user returns 404 error."""
    auth_user_id = "1"
    await create_user(client, auth_user_id)
    client.set_auth_user_id(auth_user_id)
    fake_user_id = uuid4()

    error = (await client.read_user(fake_user_id)).assert_status(404).unwrap_err()

    assert error.code == "USER_NOT_FOUND"
    assert error.meta is not None
    assert "user_id" in error.meta
    assert error.meta["user_id"] == str(fake_user_id)


async def test_by_other_user(client: APIClient) -> None:
    """Test that reading another user's data returns 403 error."""
    first_auth_user_id = "1"
    second_auth_user_id = "2"
    first_user_id = await create_user(client, first_auth_user_id)
    await create_user(client, auth_user_id=second_auth_user_id)
    client.set_auth_user_id(second_auth_user_id)

    error = (await client.read_user(first_user_id)).assert_status(403).unwrap_err()

    assert error.code == "ACCESS_DENIED"


async def test_unauthorized(client: APIClient) -> None:
    """Test that reading a user without authentication returns 401 error."""
    user_id = uuid4()
    error = (await client.read_user(user_id)).assert_status(401).unwrap_err()

    assert error.code == "UNAUTHORIZED"
