from crudik.adapters.api_client import APIClient
from crudik.entities.common.identifiers import UserId


async def create_user(api_client: APIClient) -> UserId:
    """Create a user via API and return its id."""
    response = await api_client.create_user()
    user_id = response.assert_status(200).ensure_ok().id

    return user_id
