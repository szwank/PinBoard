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
        """
        Create user

        :param active: determine if created user will be active.
            Don't set is_active in kwargs as this will throw an error.
        :param kwargs: other user values
        """
        if kwargs.get("is_active"):
            raise ValueError(
                "Cannot pass is_active in kwargs. Pass arg active=True instead."
            )
        if active:
            kwargs["is_active"] = True

        user = baker.make("users.User", **kwargs)
        return user
