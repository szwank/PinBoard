from django.shortcuts import (
    redirect,
)
from django_filters import (
    rest_framework as filters,
)
from rest_framework import (
    permissions,
)
from rest_framework.generics import (
    GenericAPIView,
    get_object_or_404,
)
from rest_framework.renderers import (
    TemplateHTMLRenderer,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from tasks.filtersets import (
    EpicFilter,
    TaskFilter,
)
from tasks.models import (
    Epic,
    Task,
)
from tasks.serializers import (
    EpicSerializer,
    NewTaskSerializer,
    TaskSerializer,
)


class TasksViewSet(ModelViewSet):
    """Operate on user tasks"""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.action == "create":
            return NewTaskSerializer
        else:
            return super().get_serializer_class()

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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EpicFilter

    def get_queryset(self):
        """Return user Epics"""
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        """Add current user to the serializer"""
        serializer.save(user=self.request.user)


class EditTask(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tasks/edit_task.html"
    serializer_class = TaskSerializer
    swagger_schema = None

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = self.get_serializer(task)
        return Response({"serializer": serializer, "task": task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = self.get_serializer(task, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "task": task})
        serializer.save()
        return redirect("core:index")


class CreateTask(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tasks/create_task.html"
    serializer_class = NewTaskSerializer
    swagger_schema = None

    def get(self, request):
        serializer = self.get_serializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        serializer.save(user=self.request.user)
        return redirect("core:index")


class EditEpic(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tasks/edit_epic.html"
    serializer_class = EpicSerializer
    swagger_schema = None

    def get(self, request, pk):
        epic = get_object_or_404(Epic, pk=pk)
        serializer = self.get_serializer(epic)
        return Response({"serializer": serializer, "epic": epic})

    def post(self, request, pk):
        epic = get_object_or_404(Epic, pk=pk)
        serializer = self.get_serializer(epic, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "epic": epic})
        serializer.save()
        return redirect("core:index")


class CreateEpic(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tasks/create_epic.html"
    serializer_class = EpicSerializer
    swagger_schema = None

    def get(self, request):
        serializer = self.get_serializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        serializer.save(user=self.request.user)
        return redirect("core:index")
