from bazario import Notification

from crudik.domain.identifiers import UserId


class UserCreated(Notification):
    def __init__(self, user_id: UserId) -> None:
        self.user_id = user_id
