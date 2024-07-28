from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from cash_collector.core.models import TimeStampModelMixin
from cash_collector.users.models import CashCollector

# Create your models here.





class Task(TimeStampModelMixin):
    class Status(models.IntegerChoices):
        PENDING = 1, _("pending")
        COLLECTED = 2, _("collected")
        DELIVERED = 3, _("delivered")
        PARTIALLY_COLLECTED = 4, _("partially_collected")

    cash_collector = models.ForeignKey(
        CashCollector, on_delete=models.CASCADE, related_name="tasks"
    )
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_due_at = models.DateTimeField()
    status = models.PositiveSmallIntegerField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )  # noqa: E501v

    def __str__(self):
        return f"{self.customer_name} - {self.amount_due}"

    def clean(self):
        if not self.cash_collector.manager:
            msg = _(
                "task_error_message_to_say_you_cannot_assign_this_task_to_this_user_because_they_do_not_have_a_manager"
            )
            return ValidationError(msg)
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

@receiver(pre_save, sender=Task)
def validate_task(sender, instance, **kwargs):
    if not instance.cash_collector.manager:
        from django.core.exceptions import ValidationError
        msg = "task_error_message_to_say_you_cannot_assign_this_task_to_this_user_because_they_do_not_have_a_manager"  # noqa: E501
        raise ValidationError(msg)
