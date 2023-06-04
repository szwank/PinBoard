from model_bakery import (
    baker,
)

from tasks.models import (
    Task,
)


class TaskFactory:
    """Task factory"""

    @staticmethod
    def create_new_task(**kwargs) -> Task:
        """Create new Task (with status = Opened)"""
        user = baker.make("tasks.Task", status=Task.StatusType.OPENED, **kwargs)
        return user

    @staticmethod
    def create_task(**kwargs) -> Task:
        """Create a Task"""
        user = baker.make("tasks.Task", **kwargs)
        return user
