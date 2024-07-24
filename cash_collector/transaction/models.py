from django.db import models

from cash_collector.core.models import TimeStampModelMixin
from cash_collector.users.models import CashCollector

# Create your models here.


class Transaction(TimeStampModelMixin):
    TRANSACTION_TYPES = [
        ("collect", "Collect"),
        ("deliver", "Deliver"),
    ]

    cash_collector = models.ForeignKey(
        CashCollector, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    def __str__(self):
        return (
            f"{self.cash_collector.username} - {self.amount} - {self.transaction_type}"
        )
