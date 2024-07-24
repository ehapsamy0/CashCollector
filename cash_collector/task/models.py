from django.db import models

from cash_collector.core.models import TimeStampModelMixin
from cash_collector.users.models import CashCollector

# Create your models here.


class Task(TimeStampModelMixin):
    cash_collector = models.ForeignKey(
        CashCollector, on_delete=models.CASCADE, related_name="tasks"
    )
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due_at = models.DateTimeField()
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.customer_name} - {self.amount_due}"
