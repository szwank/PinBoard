from rest_framework.routers import (
    DefaultRouter,
)

from users.views import (
    UserViewSet,
)

app_name = "users"

router_v1 = DefaultRouter()
router_v1.register("", UserViewSet)

urlpatterns = []

urlpatterns += router_v1.urls
