from http import (
    HTTPStatus,
)

import pytest
from django.urls import (
    reverse,
)

from tasks.models import (
    Epic,
    Task,
)
from tasks.tests.factories import (
    EpicFactory,
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


@pytest.mark.django_db
class TestEpicViewSet:
    """Test Epic views"""

    def test_create_epic(self, client, user):
        """Verify Epic creation"""

        data = {
            "title": "This is nice title",
        }
        client.force_authenticate(user)
        response = client.post(reverse("tasks:epic-list"), data=data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.data["title"] == data["title"]
        assert response.data["user"] == UserSerializer(user).data

    def test_anonymous_cannot_create_epic(self, client, user):
        """Assert anonymous user cannot create an epic"""
        data = {
            "title": "This is nice title",
        }
        response = client.post(reverse("tasks:epic-list"), data=data)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.data

    def test_list_tasks_by_epic(self, client, user_fixture_factory):
        """Verify if user see only their epic"""
        owner = user_fixture_factory()
        some_user = user_fixture_factory()

        user_epics = EpicFactory.create_epic(user=owner, _quantity=2)
        other_user_epic = EpicFactory.create_epic(user=some_user)

        client.force_authenticate(owner)
        response = client.get(reverse("tasks:epic-list"))

        assert response.status_code == HTTPStatus.OK, response.data
        epic_ids = {epic["id"] for epic in response.data}
        assert {
            epic.id for epic in user_epics
        } == epic_ids, "User should see only all their epics"
        assert (
            other_user_epic.id not in epic_ids
        ), "Other user epics should not be seen by user"

    def test_user_see_only_their_epics(self, client, user_fixture_factory):
        """Assert that user see only their epics"""
        owner = user_fixture_factory()
        some_user = user_fixture_factory()

        owner_epics = EpicFactory.create_epic(user=owner, _quantity=2)
        some_user_epic = EpicFactory.create_epic(user=some_user)

        client.force_authenticate(owner)
        response = client.get(reverse("tasks:epic-list"))

        assert response.status_code == HTTPStatus.OK, response.data
        epic_ids = {epic["id"] for epic in response.data}
        assert {
            epic.id for epic in owner_epics
        } == epic_ids, "User should see only all their epics"
        assert (
            some_user_epic.id not in epic_ids
        ), "Other user epics should not be seen by user"

    def test_anonymous_user_dont_see_epics(self, client, user):
        """Verify that anonymous user don't see any epic"""

        EpicFactory.create_epic(user=user, _quantity=2)

        response = client.get(reverse("tasks:task-list"))

        assert response.status_code == HTTPStatus.OK, response.data
        assert len(response.data) == 0, "Anonymous user should not see any epics"

    def test_update_epic(self, client, user):
        """Verify updating epic by user"""
        epic = EpicFactory.create_epic(user=user, title="Old title")

        new_title = "New title"
        client.force_authenticate(user)
        response = client.patch(
            reverse("tasks:epic-detail", args=[epic.id]),
            data={"title": new_title},
        )

        assert response.status_code == HTTPStatus.OK

        epic.refresh_from_db()
        assert epic.title == new_title

    def test_task_can_be_updated_only_by_owner(self, client, user_fixture_factory):
        """Assert epics can be only updated by user that created the epic"""
        owner = user_fixture_factory()
        some_user = user_fixture_factory()

        old_title = "Old title"
        epic = EpicFactory.create_epic(user=owner, title=old_title)

        client.force_authenticate(some_user)
        response = client.patch(
            reverse("tasks:epic-detail", args=[epic.id]),
            data={"title": "New Title"},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        epic.refresh_from_db()
        assert epic.title == old_title

    def test_update_task_by_anonymous_user(self, client, user):
        """Assert anonymous user cannot update epic"""
        old_title = "Old title"
        epic = EpicFactory.create_epic(user=user, title=old_title)

        response = client.patch(
            reverse("tasks:epic-detail", args=[epic.id]),
            data={"title": "New title"},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        epic.refresh_from_db()
        assert epic.title == old_title

    def test_remove_task(self, client, user):
        """Verify removing tasks by user"""
        epic = EpicFactory.create_epic(user=user)

        client.force_authenticate(user)
        response = client.delete(
            reverse("tasks:epic-detail", args=[epic.id]),
        )

        assert response.status_code == HTTPStatus.NO_CONTENT

        assert not Epic.objects.filter(id=epic.id).exists()

    def test_remove_task_by_anonymous_user(self, client, user):
        """Verify removing tasks by user"""
        epic = EpicFactory.create_epic(user=user)

        response = client.delete(
            reverse("tasks:epic-detail", args=[epic.id]),
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
