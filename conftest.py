import pytest
from django.contrib.auth import (
    get_user_model,
)
from rest_framework.test import (
    APIClient,
)

from users.tests.factories import (
    UserFactory,
)


@pytest.fixture
def user_class():
    """Get currently user model class fixture"""

    return get_user_model()


@pytest.fixture
def user_fixture_factory():
    """Fake user fixture factory"""
    return UserFactory.create_user


@pytest.fixture
def user():
    """Create and return user"""
    return UserFactory.create_user()


@pytest.fixture
def client():
    """Return test client"""
    return APIClient()
