from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import (
    models,
)
from django.db.models import (
    QuerySet,
)
from django.utils.translation import (
    gettext_lazy as _,
)

from tasks.models import (
    Epic,
    Task,
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
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    REQUIRED_FIELDS = ["email", "first_name", "last_name", "sex"]

    objects = UserManager()

    def tasks(self, status: Task.StatusType = None) -> QuerySet[Task]:
        """
        Return user tasks.

        :param status: if set only tasks with given status will be returned.
        """
        queryset = self.user_tasks

        if status:
            queryset = queryset.filter(status=status)
        else:
            queryset = queryset.all()

        return queryset.all()

    def epics(self) -> QuerySet[Epic]:
        """Return user epics."""
        return self.user_epics.all()
