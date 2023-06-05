from rest_framework.routers import (
    DefaultRouter,
)

from tasks import (
    views,
)

app_name = "tasks"

router_v1 = DefaultRouter()
router_v1.register("", views.TasksViewSet)

urlpatterns = []

urlpatterns += router_v1.urls
