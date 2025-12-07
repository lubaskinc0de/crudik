from crudik.entities.common.identifiers import UserId
from tests.integration.api_client import APIClient


async def create_user(client: APIClient) -> UserId:
    """Create a user via API and return its id."""
    response = await client.create_user()
    user_id = response.assert_status(200).ensure_ok().id

    return user_id
