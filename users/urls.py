from rest_framework.routers import (
    DefaultRouter,
)

from users import (
    views,
)

app_name = "users"

router_v1 = DefaultRouter()
router_v1.register("", views.UserViewSet)

urlpatterns = []

urlpatterns += router_v1.urls
