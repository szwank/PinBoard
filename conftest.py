import pytest
from django.contrib.auth import (
    get_user_model,
)


@pytest.fixture
def user_class():
    """Get currently user model class fixture"""

    return get_user_model()
