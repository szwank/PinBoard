from django_filters import (
    rest_framework as filters,
)

from tasks.models import (
    Epic,
    Task,
)


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            "title": ["contains"],
            "description": ["contains"],
            "status": ["exact"],
        }


class EpicFilter(filters.FilterSet):
    class Meta:
        model = Epic
        fields = {
            "title": ["contains"],
        }
