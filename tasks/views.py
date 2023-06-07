from rest_framework import (
    permissions,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from tasks.models import (
    Epic,
    Task,
)
from tasks.serializers import (
    EpicSerializer,
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

    def perform_create(self, serializer):
        """Add current user to the serializer"""
        serializer.save(user=self.request.user)


class EpicViewSet(ModelViewSet):
    """Operate on user epics"""

    serializer_class = EpicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Epic.objects.all()

    def get_queryset(self):
        """Return user Epics"""
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        """Add current user to the serializer"""
        serializer.save(user=self.request.user)
