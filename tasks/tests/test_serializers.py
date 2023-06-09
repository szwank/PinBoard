import pytest
import rest_framework.exceptions

from core.test_utils import (
    FakeRequest,
)
from tasks.models import (
    Task,
)
from tasks.serializers import (
    EpicSerializer,
    NewTaskSerializer,
    TaskSerializer,
)
from tasks.tests.factories import (
    EpicFactory,
    TaskFactory,
)


@pytest.mark.django_db
class TestTaskSerializer:
    """Test Task serialization"""

    def test_create_new_task(self, user):
        """Verify Task creation"""

        data = {
            "title": "Test title",
            "description": "Do this and do that",
            "epic_id": None,
        }

        task_serializer = NewTaskSerializer(
            data=data, context={"request": FakeRequest(user)}
        )

        task_serializer.is_valid(raise_exception=True)
        task = task_serializer.save(user=user)

        assert task.title == data["title"]
        assert task.description == data["description"]
        assert task.status == Task.StatusType.OPENED
        assert task.user == user

    def test_create_new_task_with_epic(self, user):
        """Verify creation of Task with Epic"""
        epic = EpicFactory.create_epic(user=user)
        data = {
            "title": "Test title",
            "description": "Do this and do that",
            "epic_id": str(epic.id),
        }

        task_serializer = NewTaskSerializer(
            data=data, context={"request": FakeRequest(user)}
        )

        task_serializer.is_valid(raise_exception=True)
        task = task_serializer.save(user=user)

        assert task.title == data["title"]
        assert task.description == data["description"]
        assert task.status == Task.StatusType.OPENED
        assert task.epic == epic
        assert task.user == user

    def test_cannot_create_ticket_with_status(self, user):
        """Assert task will not be created when status is passed"""

        data = {
            "title": "Does not matter",
            "description": "Does not matter",
            "status": Task.StatusType.INPROGRES,
        }

        task_serializer = NewTaskSerializer(
            data=data, context={"request": FakeRequest(user)}
        )

        with pytest.raises(rest_framework.exceptions.ValidationError):
            task_serializer.is_valid(raise_exception=True)

    def test_cannot_update_with_NewTaskSerializer(self, user):
        """Assert task cannot be updated with NewTaskSerializer"""
        task = TaskFactory.create_new_task()
        data = {
            "title": "Does not matter",
            "description": "Does not matter",
            "status": Task.StatusType.INPROGRES,
        }

        task_serializer = NewTaskSerializer(
            data, context={"request": FakeRequest(user)}
        )
        with pytest.raises(NotImplementedError):
            task_serializer.update(task, data)

    def test_assert_cannot_create_ticket_with_status(self, user):
        """Assert cannot create new task with TaskSerializer"""

        data = {
            "title": "Does not matter",
            "description": "Does not matter",
            "status": Task.StatusType.INPROGRES,
            "epic_id": None,
        }

        task_serializer = TaskSerializer(
            data=data, context={"request": FakeRequest(user)}
        )
        task_serializer.is_valid(raise_exception=True)

        with pytest.raises(NotImplementedError):
            task_serializer.save()

    def test_serialize_task(self, user):
        """Verify Task serialization"""

        task = TaskFactory.create_new_task(user=user)

        task_serializer = TaskSerializer(task, context={"request": FakeRequest(user)})

        data = task_serializer.data
        assert task.title == data["title"]
        assert task.description == data["description"]
        assert task.status == Task.StatusType.OPENED
        assert task.user == user

    def test_updating_task(self, user):
        """Varify Task Update"""

        update_data = {
            "title": "New title",
            "description": "New description",
            "status": Task.StatusType.INPROGRES,
        }

        task = TaskFactory.create_task(
            user=user, title="Old title", description="Old description"
        )

        task_serializer = TaskSerializer(
            data=update_data, partial=True, context={"request": FakeRequest(user)}
        )
        task_serializer.is_valid(raise_exception=True)

        task_serializer.update(task, update_data)

        assert task.title == update_data["title"]
        assert task.description == update_data["description"]
        assert task.status == update_data["status"]
        assert task.user == user

    def test_assert_user_cannot_be_changed(self, user_fixture_factory):
        """Verify Task creation"""

        user = user_fixture_factory()
        new_user = user_fixture_factory()
        update_data = {"user": new_user}

        task = TaskFactory.create_task(
            user=user, title="Old title", description="Old description"
        )

        task_serializer = TaskSerializer(
            data=update_data, partial=True, context={"request": FakeRequest(user)}
        )
        task_serializer.is_valid(raise_exception=True)

        with pytest.raises(rest_framework.exceptions.ValidationError):
            task_serializer.update(task, update_data)


@pytest.mark.django_db
class TestEpicSerializer:
    """Test Task serialization"""

    def test_create_new_epic(self, user):
        """Verify Epic creation"""

        data = {
            "title": "Test title",
        }

        epic_serializer = EpicSerializer(
            data=data, context={"request": FakeRequest(user)}
        )

        epic_serializer.is_valid(raise_exception=True)
        epic = epic_serializer.save(user=user)

        assert epic.title == data["title"]
        assert epic.user == user

    def test_serialize_epic(self, user):
        """Verify Epic serialization"""

        epic = EpicFactory.create_epic(user=user)

        epic_serializer = EpicSerializer(epic)

        data = epic_serializer.data
        assert epic.title == data["title"]
        assert epic.user == user

    def test_updating_epic(self, user):
        """Varify Epic update"""

        update_data = {
            "title": "New title",
        }

        epic = EpicFactory.create_epic(user=user, title="Old title")

        epic_serializer = EpicSerializer(data=update_data, partial=True)
        epic_serializer.is_valid(raise_exception=True)

        epic_serializer.update(epic, update_data)

        assert epic.title == update_data["title"]
        assert epic.user == user

    def test_assert_user_cannot_be_changed(self, user_fixture_factory):
        """Verify Epic creation"""

        user = user_fixture_factory()
        new_user = user_fixture_factory()
        update_data = {"user": new_user}

        epic = EpicFactory.create_epic(
            user=user,
            title="Old title",
        )

        epic_serializer = EpicSerializer(data=update_data, partial=True)
        epic_serializer.is_valid(raise_exception=True)

        with pytest.raises(rest_framework.exceptions.ValidationError):
            epic_serializer.update(epic, update_data)
