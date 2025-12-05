from crudik.adapters.auth.model import AuthUserId
from crudik.entities.common.identifiers import UserId
from tests.integration.api_client import APIClient


async def create_user(client: APIClient, auth_user_id: AuthUserId) -> UserId:
    """Create a user via API and return its id."""
    client.set_auth_user_id(auth_user_id)
    user_id = (await client.create_user()).assert_status(200).unwrap().id
    client.reset_auth_user_id()
    return user_id
