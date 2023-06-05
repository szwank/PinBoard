from django.utils.translation import (
    gettext_lazy as _,
)
from rest_framework import (
    serializers,
)
from rest_framework.exceptions import (
    ValidationError,
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


class SetUserMixIn(metaclass=serializers.SerializerMetaclass):
    """Mixin implementing setting current user to field user"""

    user_id = serializers.IntegerField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.fields += ["user_id", "user"]
        self.default_error_messages.update(
            {"user_not_found": _("User with given id does not exist")}
        )

    def validate_user_id(self, value):
        """Check if user exists"""
        user = User.objects.filter(id=value).first()
        if user is None:
            error_code = "user_not_found"
            raise ValidationError(
                detail=self.error_messages[error_code], code=error_code
            )
        self.user = user  # this should not be done here, but not found better solution
        return value
