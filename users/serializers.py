from rest_framework import (
    serializers,
)

from users.models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "sex"]
        depth = 1
        ref_name = "User serializer"
