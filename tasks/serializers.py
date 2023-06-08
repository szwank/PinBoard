from django.contrib.auth import (
    get_user_model,
)
from django.utils.translation import (
    gettext_lazy as _,
)
from rest_framework import (
    serializers,
)
from rest_framework.fields import (
    CurrentUserDefault,
)

from tasks.models import (
    Epic,
    Task,
)
from users.serializers import (
    UserSerializer,
)

User = get_user_model()


class EpicSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    default_error_messages = {
        "cannot_update_user": _("User cannot be updated"),
    }

    class Meta:
        model = Epic
        fields = ["id", "user", "title"]
        depth = 1

    def create(self, validated_data):
        return Epic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("user"):
            error_code = "cannot_update_user"
            self.fail(error_code)

        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status = serializers.ChoiceField(choices=Task.StatusType, required=False)
    # choices set dynamically in the init
    epic_id = serializers.ChoiceField(choices=[], write_only=True, allow_null=True)
    epic = EpicSerializer(read_only=True)

    default_error_messages = {
        "cannot_update_user": _("User cannot be updated"),
        "status_cannot_be_set": _("Status cannot be set when creating a Task"),
    }

    class Meta:
        model = Task
        fields = ["id", "user", "title", "description", "status", "epic", "epic_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if not user.is_anonymous:
            self.fields["epic_id"].choices = [
                (epic.id, epic.title) for epic in self.context["request"].user.epics()
            ]

    def create(self, validated_data):
        raise NotImplementedError(
            "Should not be called. To create task use NewTaskSerializer instead."
        )

    def update(self, instance, validated_data):
        if validated_data.get("user"):
            error_code = "cannot_update_user"
            self.fail(error_code)

        return super().update(instance, validated_data)


class NewTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    # choices set dynamically in the init
    epic_id = serializers.ChoiceField(choices=[], write_only=True, allow_null=True)
    epic = EpicSerializer(read_only=True)

    default_error_messages = {
        "status_cannot_be_set": _("Status cannot be set when creating a Task"),
    }

    class Meta:
        model = Task
        fields = ["id", "user", "title", "description", "status", "epic", "epic_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if not user.is_anonymous:
            self.fields["epic_id"].choices = [
                (epic.id, epic.title) for epic in self.context["request"].user.epics()
            ]

    def validate(self, attrs):
        """
        Validate that status was not passed.

        This is mostly done to throw up usefully message in case status is passed.
        """
        if hasattr(self, "initial_data"):
            if self.initial_data.get("status"):
                error_code = "status_cannot_be_set"
                self.fail(error_code)

        return super().validate(attrs)

    def create(self, validated_data):
        return Task.objects.create(status=Task.StatusType.OPENED, **validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "Should not be called. To update task use TaskSerializer instead."
        )
