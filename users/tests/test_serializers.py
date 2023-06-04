import pytest

from users.serializers import (
    UserSerializer,
)


@pytest.mark.django_db
class TestSerializers:
    """Test users app serializers"""

    def test_user_serializer(self, user_fixture_factory):
        """Verify User serializer"""

        user = user_fixture_factory(active=True)
        user_serializer = UserSerializer(user)

        assert user_serializer.data["id"] == user.id
        assert user_serializer.data["username"] == user.username
        assert user_serializer.data["email"] == user.email
        assert user_serializer.data["first_name"] == user.first_name
        assert user_serializer.data["last_name"] == user.last_name
