from django.contrib.auth import (
    get_user_model,
)
from model_bakery import (
    baker,
)

User = get_user_model()


class UserFactory:
    @staticmethod
    def create_user(**kwargs) -> User:
        kwargs.setdefault("is_active", True)

        user = baker.make("users.User", **kwargs)
        return user
