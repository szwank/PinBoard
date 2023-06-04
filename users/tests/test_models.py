import pytest


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
