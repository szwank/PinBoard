from rest_framework.routers import (
    DefaultRouter,
)

from tasks import (
    views,
)

app_name = "tasks"

router_v1 = DefaultRouter()
router_v1.register("tasks", views.TasksViewSet)
router_v1.register("epics", views.EpicViewSet)

urlpatterns = []

urlpatterns += router_v1.urls
