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
            user_tasks = "user_tasks"
            user_epics = "user_epics"

            context[user_tasks] = self.request.user.tasks()
            task_search = self.request.GET.get("task_search", False)
            if task_search:
                context[user_tasks] = (
                    context[user_tasks].filter(title__contains=task_search).all()
                )

            context[user_epics] = self.request.user.epics()
            epic_search = self.request.GET.get("epic_search", False)
            if epic_search:
                context[user_epics] = (
                    context[user_epics].filter(title__contains=epic_search).all()
                )
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
