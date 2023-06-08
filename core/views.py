from django.views.generic import (
    TemplateView,
)


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context["user_tasks"] = self.request.user.tasks()
            context["user_epics"] = self.request.user.epics()
        return context
