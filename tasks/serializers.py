from django.contrib.auth import (
    get_user_model,
)
from django.utils.translation import (
    gettext_lazy as _,
)
from rest_framework import (
    serializers,
)
from rest_framework.exceptions import (
    ValidationError,
)

from tasks.models import (
    Task,
)
from users.serializers import (
    UserSerializer,
)

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    status = serializers.CharField(required=False)

    default_error_messages = {
        "user_not_found": _("User with given id does not exist"),
        "not_logged_in": _("Only logged_in users can create a Task"),
        "cannot_update_user": _("User cannot be updated"),
        "status_cannot_be_set": _("Status cannot be set when creating a Task"),
    }

    class Meta:
        model = Task
        fields = ["id", "user", "title", "description", "status", "user_id"]
        depth = 1

    def create(self, validated_data):
        if validated_data.get("status"):
            error_code = "status_cannot_be_set"
            self.fail(error_code)

        return Task.objects.create(
            status=Task.StatusType.OPENED, user=self.user, **validated_data
        )

    def update(self, instance, validated_data):
        if validated_data.get("user"):
            error_code = "cannot_update_user"
            self.fail(error_code)

        return super().update(instance, validated_data)

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
