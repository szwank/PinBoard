from django.contrib import (
    admin,
)

from tasks.models import (
    Epic,
    Task,
)

admin.site.register(Task)
admin.site.register(Epic)
