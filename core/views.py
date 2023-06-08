from django.views.generic import (
    TemplateView,
)

from tasks.models import (
    Task,
)


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context["user_tasks"] = self.request.user.tasks()
            context["user_epics"] = self.request.user.epics()
        return context


class PinBoardView(TemplateView):
    template_name = "core/pin_board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context["user_tasks_open"] = self.request.user.tasks(Task.StatusType.OPENED)
            context["user_tasks_inprogress"] = self.request.user.tasks(
                Task.StatusType.INPROGRES
            )
            context["user_tasks_done"] = self.request.user.tasks(Task.StatusType.DONE)
        return context
