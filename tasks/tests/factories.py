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
        task = baker.make("tasks.Task", status=Task.StatusType.OPENED, **kwargs)
        return task

    @staticmethod
    def create_task(**kwargs) -> Task:
        """Create a Task"""
        task = baker.make("tasks.Task", **kwargs)
        return task


class EpicFactory:
    """Epic factory"""

    @staticmethod
    def create_epic(**kwargs) -> Task:
        """Create a Task"""
        epic = baker.make("tasks.Epic", **kwargs)
        return epic
