import pytest
from django.core.management import (
    call_command,
)


@pytest.mark.django_db
class TestCommandCreatedefaultsuperuser:
    def test_creating_super_user(self, user_class):
        """Verify creation of super user"""
        call_command("createdefaultsuperuser")
        user = user_class.objects.filter(username="admin").first()

        assert user.is_active is True
        assert user.is_staff is True
        assert user.is_superuser is True
