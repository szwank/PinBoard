from django.urls import (
    path,
)

from core.views import (
    IndexView,
    PinBoardView,
)
from tasks.views import (
    CreateEpic,
    CreateTask,
    EditEpic,
    EditTask,
)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("pinboard", PinBoardView.as_view(), name="pin_board"),
    path("task/edit/<int:pk>", EditTask.as_view(), name="edit_task"),
    path("task/create/", CreateTask.as_view(), name="create_task"),
    path("epic/edit/<int:pk>", EditEpic.as_view(), name="edit_epic"),
    path("epic/create/", CreateEpic.as_view(), name="create_epic"),
]
