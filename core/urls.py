from django.urls import (
    path,
)

from core.views import (
    IndexView,
    PinBoardView,
)
from tasks.views import (
    CreateTask,
    EditTask,
)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("pinboard", PinBoardView.as_view(), name="pin_board"),
    path("task/edit/<int:pk>", EditTask.as_view(), name="edit_task"),
    path("task/create/", CreateTask.as_view(), name="create_task"),
]
