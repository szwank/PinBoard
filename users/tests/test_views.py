import json
from http import (
    HTTPStatus,
)

import pytest
from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)

from users.tests.factories import (
    UserFactory,
)


@pytest.mark.django_db
class TestUserViewSet:
    """Test user views"""

    def setup(self):
        self.data = {
            "username": "username",
            "email": "test@test.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "somepassword123",
            "re_password": "somepassword123",
            "sex": "male",
        }

    def test_creating_user(self, client, user_class):
        """Test creating user"""
        assert not user_class.objects.filter(username=self.data["username"]).exists()

        response = client.post(
            reverse("users:user-list"),
            data=json.dumps(self.data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["first_name"] == self.data["first_name"]
        assert response.data["last_name"] == self.data["last_name"]
        assert response.data["email"] == self.data["email"]
        assert response.data["sex"] == self.data["sex"]
        assert response.data["username"] == self.data["username"]
        assert response.data.get("id", False), "Id not in the response"

        user = user_class.objects.get(username=self.data["username"])
        assert user.email == self.data["email"]
        assert user.username == self.data["username"]
        assert user.first_name == self.data["first_name"]
        assert user.last_name == self.data["last_name"]
        assert user.sex == self.data["sex"]
        assert user.is_active is False

    def test_getting_user(self, client, user):
        """Test fetching user"""
        client.force_authenticate(user)
        response = client.get(
            reverse("users:user-detail", args=[user.id]),
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.OK
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name
        assert response.data["email"] == user.email
        assert response.data["sex"] == user.sex
        assert response.data["username"] == user.username
        assert response.data["id"] == user.id

    def test_user_activation(self, client):
        """Verify user activation"""
        user = UserFactory.create_user(is_active=False, username="Jack")
        response = client.get(
            reverse("users:user-activate-user", args=[user.username]),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data == {}
        user.refresh_from_db()
        assert user.is_active is True
