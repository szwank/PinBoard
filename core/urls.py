from django.urls import (
    path,
)

from core.views import (
    IndexView,
    PinBoardView,
)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("pinboard", PinBoardView.as_view(), name="pin_board"),
]
