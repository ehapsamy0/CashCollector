from django.db import models

# Create your models here.


class TimeStampModelMixin(models.Model):
    """
    timestamp (created, updated) fields mixin
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created datetime")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="last modified datetime")

    class Meta:  # pylint: disable=C0115, R0903
        abstract = True
