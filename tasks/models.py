from django.contrib.auth import (
    get_user_model,
)
from django.db import (
    models,
)

from core.models import (
    DatesModelMixin,
)

User = get_user_model()


class Task(DatesModelMixin):
    """User task"""

    class StatusType(models.TextChoices):
        """Allowed statuses"""

        OPENED = "Opened"
        INPROGRES = "In Progress"
        DONE = "Done"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tasks")
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusType.choices)
