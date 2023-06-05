from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_yasg import (
    openapi,
)
from drf_yasg.utils import (
    swagger_auto_schema,
)
from rest_framework import (
    permissions,
    status,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import (
    APIView,
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
    EpicTasksSerializer,
    TaskSerializer,
)


class TasksViewSet(ModelViewSet):
    """Operate on user tasks"""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        """Return user Tasks"""
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=self.request.user).all()

    def create(self, request, *args, **kwargs):
        request.data["user_id"] = request.user.id
        return super().create(request, *args, **kwargs)


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

    def create(self, request, *args, **kwargs):
        request.data["user_id"] = request.user.id
        return super().create(request, *args, **kwargs)


class ListTaskApiView(APIView):
    filter_backends = [DjangoFilterBackend]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("title", openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={"200": openapi.Response("Model", TaskSerializer(many=True))},
    )
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({})

        assert len(args) == 1
        queryset = Task.objects
        if epic_title:
            queryset = queryset.filter("task__epic_id" == args)

        serializer = TaskSerializer(queryset.all(), many=True)
        return Response(serializer.data)
