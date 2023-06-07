import pytest

from tasks.models import (
    Task,
)
from tasks.tests.factories import (
    EpicFactory,
    TaskFactory,
)


@pytest.mark.django_db
class TestModels:
    """Test users app models"""

    def test_create_user(self, user_class):
        """Verify custom user object creation"""
        username = "user"
        email = "user@user.com"
        password = "foo"
        first_name = "John"
        last_name = "Doe"

        user = user_class.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        assert user.username == username
        assert user.check_password(password)
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.is_active is False
        assert not user.is_staff
        assert not user.is_superuser

    def test_creating_normal_user_with_superuser_true(self, user_class):
        """
        Verify that user is not created if is_superuser kwarg is set
        to True.
        """

        with pytest.raises(
            ValueError, match="User cannot have set is_superuser=True.*"
        ):
            user_class.objects.create_user(
                username="username",
                email="user@user.com",
                password="foo",
                first_name="John",
                last_name="Doe",
                is_superuser=True,
            )

    def test_create_superuser(self, user_class):
        """Verify superuser object creation"""

        username = "user"
        email = "user@user.com"
        password = "foo"
        first_name = "John"
        last_name = "Doe"

        user = user_class.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.username == username
        assert user.check_password(password)
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_create_superuser_when_superuser_is_false(self, user_class):
        """
        Verify that superuser is not created if is_superuser kwarg is set
        to false
        """

        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            user_class.objects.create_superuser(
                email="user@user.com", password="foo", is_superuser=False
            )

    def test_create_superuser_when_staff_is_false(self, user_class):
        """
        Verify that superuser is not created if is_staff kwarg is set
        to false
        """

        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            user_class.objects.create_superuser(
                email="user@user.com", password="foo", is_staff=False
            )

    def test_getting_user_tasks(self, user):
        """Verify fetching user tasks"""
        tasks_to_find = TaskFactory.create_task(user=user, _quantity=3)
        TaskFactory.create_task(_quantity=3)  # other tasks

        user_tasks = user.tasks()

        assert set(user_tasks) == set(tasks_to_find)

    def test_getting_user_tasks_with_chosen_status(self, user):
        """Verify fetching user tasks with chosen status"""
        task_to_find = TaskFactory.create_task(user=user, status=Task.StatusType.OPENED)
        TaskFactory.create_task(user=user, status=Task.StatusType.INPROGRES)
        TaskFactory.create_task(user=user, status=Task.StatusType.DONE)

        opened_tasks = user.tasks(Task.StatusType.OPENED)

        assert len(opened_tasks) == 1, "Should return only one task"
        assert opened_tasks[0] == task_to_find

    def test_getting_user_epics(self, user):
        """Verify fetching user epics"""
        epics_to_find = EpicFactory.create_epic(user=user, _quantity=3)
        TaskFactory.create_task(_quantity=3)  # other tasks

        user_epics = user.epics()

        assert set(user_epics) == set(epics_to_find)
