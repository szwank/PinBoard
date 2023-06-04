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
