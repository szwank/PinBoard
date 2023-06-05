from http import (
    HTTPStatus,
)

import pytest
from django.urls import (
    reverse,
)

from tasks.models import (
    Task,
)
from tasks.tests.factories import (
    TaskFactory,
)
from users.serializers import (
    UserSerializer,
)


@pytest.mark.django_db
class TestTaskViewSet:
    """Test Task views"""

    def test_create_task(self, client, user):
        """Verify task creation"""

        data = {
            "title": "This is nice title",
            "description": "Boring description",
        }
        client.force_authenticate(user)
        response = client.post(reverse("tasks:task-list"), data=data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status"] == Task.StatusType.OPENED
        assert response.data["user"] == UserSerializer(user).data

    def test_anonymous_cannot_create_task(self, client, user):
        """Assert anonymous user cannot create a task"""
        data = {
            "title": "This is nice title",
            "description": "Boring description",
        }
        response = client.post(reverse("tasks:task-list"), data=data)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.data

    def test_list_tasks_by_user(self, client, user_fixture_factory):
        """Verify if user see only their tasks"""
        user = user_fixture_factory()
        other_user = user_fixture_factory()

        user_tasks = TaskFactory.create_task(user=user, _quantity=2)
        other_user_task = TaskFactory.create_task(user=other_user)

        client.force_authenticate(user)
        response = client.get(reverse("tasks:task-list"))

        assert response.status_code == HTTPStatus.OK, response.data
        task_ids = {task["id"] for task in response.data}
        assert {
            task.id for task in user_tasks
        } == task_ids, "User should see only all their tasks"
        assert (
            other_user_task.id not in task_ids
        ), "Other user tasks should not be seen by user"

    def test_anonymous_user_dont_see_tasks(self, client, user):
        """Verify that anonymous user don't see any task"""

        TaskFactory.create_task(user=user, _quantity=2)

        response = client.get(reverse("tasks:task-list"))

        assert response.status_code == HTTPStatus.OK, response.data
        assert len(response.data) == 0, "Anonymous user should not see any tasks"

    def test_update_task(self, client, user):
        """Verify updating task by user"""
        task = TaskFactory.create_new_task(user=user)
        assert task.status == task.StatusType.OPENED

        client.force_authenticate(user)
        response = client.patch(
            reverse("tasks:task-detail", args=[task.id]),
            data={"status": Task.StatusType.INPROGRES},
        )

        assert response.status_code == HTTPStatus.OK

        task.refresh_from_db()
        assert task.status == task.StatusType.INPROGRES

    def test_update_task_by_anonymous_user(self, client, user):
        """Assert anonymous user cannot update task"""
        task = TaskFactory.create_new_task(user=user)
        assert task.status == task.StatusType.OPENED

        response = client.patch(
            reverse("tasks:task-detail", args=[task.id]),
            data={"status": Task.StatusType.INPROGRES},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        task.refresh_from_db()
        assert task.status == task.StatusType.OPENED

    def test_remove_task(self, client, user):
        """Verify removing tasks by user"""
        task = TaskFactory.create_new_task(user=user)

        client.force_authenticate(user)
        response = client.delete(
            reverse("tasks:task-detail", args=[task.id]),
        )

        assert response.status_code == HTTPStatus.NO_CONTENT

        assert not Task.objects.filter(id=task.id).exists()

    def test_remove_task_by_anonymous_user(self, client, user):
        """Verify removing tasks by user"""
        task = TaskFactory.create_new_task(user=user)

        response = client.delete(
            reverse("tasks:task-detail", args=[task.id]),
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
