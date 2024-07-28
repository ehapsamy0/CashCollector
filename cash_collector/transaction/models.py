from django.db import models
from django.utils.translation import gettext_lazy as _

from cash_collector.core.models import TimeStampModelMixin
from cash_collector.task.models import Task
from cash_collector.users.models import CashCollector

# Create your models here.


class Transaction(TimeStampModelMixin):
    class Type(models.IntegerChoices):
        COLLECT = 1, _("collect")
        DELIVER = 2, _("deliver")

    cash_collector = models.ForeignKey(
        CashCollector, on_delete=models.CASCADE, related_name="transactions",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.PositiveSmallIntegerField(
        choices=Type.choices, default=Type.COLLECT
    )
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return (
            f"{self.cash_collector.username} - {self.amount} - {self.transaction_type}"
        )


