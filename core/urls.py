from django.urls import (
    path,
)

from core.views import (
    IndexView,
    PinBoardView,
)
from tasks.views import (
    TaskEdit,
)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("pinboard", PinBoardView.as_view(), name="pin_board"),
    path("task/edit/<int:pk>", TaskEdit.as_view(), name="task_edit"),
]
