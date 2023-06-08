from django.db import (
    models,
)

from core.models import (
    DatesModelMixin,
)


class Task(DatesModelMixin):
    """User task"""

    class StatusType(models.TextChoices):
        """Allowed statuses"""

        OPENED = "Opened"
        INPROGRES = "In Progress"
        DONE = "Done"

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_tasks"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusType.choices)
    epic = models.ForeignKey(
        "Epic", on_delete=models.DO_NOTHING, related_name="epic_tasks", null=True
    )


class Epic(DatesModelMixin):
    """
    Epic model

    Its a label for tasks.
    """

    user = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="user_epics"
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return str(self.title)
