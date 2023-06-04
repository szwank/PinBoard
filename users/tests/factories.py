from django.contrib.auth import (
    get_user_model,
)
from model_bakery import (
    baker,
)

User = get_user_model()


class UserFactory:
    @staticmethod
    def create_user(active=True, **kwargs) -> User:
        if active:
            kwargs.update(
                {
                    "is_active": True,
                }
            )
        user = baker.make("users.User", **kwargs)
        return user
