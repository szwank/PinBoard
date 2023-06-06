from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import (
    models,
)
from django.utils.translation import (
    gettext_lazy as _,
)

from users.managers import (
    UserManager,
)


class User(AbstractUser):
    """Custom user model"""

    class SexType(models.TextChoices):
        """Sex types"""

        MALE = "male"
        FEMALE = "female"

    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    sex = models.CharField(max_length=6, choices=SexType.choices, blank=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    REQUIRED_FIELDS = ["email", "first_name", "last_name", "sex"]

    objects = UserManager()
