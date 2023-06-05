import pytest
import rest_framework.exceptions

from core.test_utils import (
    FakeRequest,
)
from tasks.models import (
    Task,
)
from tasks.serializers import (
    TaskSerializer,
)
from tasks.tests.factories import (
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
            "user_id": user.id,
        }

        task_serializer = TaskSerializer(
            data=data, context={"request": FakeRequest(user)}
        )

        task_serializer.is_valid(raise_exception=True)
        task = task_serializer.create(task_serializer.data)

        assert task.title == data["title"]
        assert task.description == data["description"]
        assert task.status == Task.StatusType.OPENED
        assert task.user == user

    def test_cannot_create_new_ticket_with_unexisting_user(self, user_class, user):
        """Assert that ticket cannot be created if unresisting user id is passed"""
        user_id = user_class.objects.latest("id").id + 1
        assert user_class.objects.filter(id=user_id).first() is None

        data = {
            "title": "Does not matter",
            "description": "Does not matter",
            "user_id": user_id,
        }

        task_serializer = TaskSerializer(
            data=data, context={"request": FakeRequest(user)}
        )

        with pytest.raises(rest_framework.exceptions.ValidationError):
            task_serializer.is_valid(raise_exception=True)

    def test_cannot_create_ticket_with_status(self, user):
        """Assert ticket will not be created when status is passed"""

        data = {
            "title": "Does not matter",
            "description": "Does not matter",
            "user_id": user.id,
            "status": Task.StatusType.OPENED,
        }

        task_serializer = TaskSerializer(
            data=data, context={"request": FakeRequest(user)}
        )
        task_serializer.is_valid(raise_exception=True)

        with pytest.raises(rest_framework.exceptions.ValidationError):
            task_serializer.create(task_serializer.data)

    def test_serialize_task(self, user):
        """Verify Task serialization"""

        task = TaskFactory.create_new_task(user=user)

        task_serializer = TaskSerializer(task)

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

        task_serializer = TaskSerializer(data=update_data, partial=True)
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

        task_serializer = TaskSerializer(data=update_data, partial=True)
        task_serializer.is_valid(raise_exception=True)

        with pytest.raises(rest_framework.exceptions.ValidationError):
            task_serializer.update(task, update_data)
