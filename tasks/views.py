from rest_framework import (
    permissions,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from tasks.models import (
    Task,
)
from tasks.serializers import (
    TaskSerializer,
)


class TasksViewSet(ModelViewSet):
    """Operate on user tasks"""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()

    def get_queryset(self):
        """Return user Tasks"""
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=self.request.user).all()

    def create(self, request, *args, **kwargs):
        request.data["user_id"] = request.user.id
        return super().create(request, *args, **kwargs)
