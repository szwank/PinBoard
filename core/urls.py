from django.urls import (
    path,
)

from core.views import (
    IndexView,
    PinBoardView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
