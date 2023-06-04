from django.db import (
    models,
)


class DatesModelMixin(models.Model):
    """
    Mixin adding creation and modification field to model.

    Additionally, models using this mixin will be sorted by created_date.
    """

    created_date = models.DateTimeField(editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_date"]
        get_latest_by = ["created_date"]
