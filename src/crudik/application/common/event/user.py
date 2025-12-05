from bazario import Notification

from crudik.entities.common.identifiers import UserId


class UserCreated(Notification):
    """Domain event notification published when a new user is being created in the system."""

    def __init__(self, user_id: UserId) -> None:
        self.user_id = user_id
