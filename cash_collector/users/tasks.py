from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from cash_collector.transaction.models import Transaction

from .models import CashCollector

User = get_user_model()


@shared_task
def check_and_freeze_cash_collectors():
    threshold_amount = 5000
    threshold_minutes = 5
    now = timezone.now()
    threshold_time = now - timedelta(days=threshold_minutes)

    collectors_to_check = CashCollector.objects.all()

    for collector in collectors_to_check:
        last_transaction = (
            Transaction.objects.filter(cash_collector=collector)
            .order_by("-created_at")
            .first()
        )
        if last_transaction and last_transaction.created_at <= threshold_time:
            if collector.balance >= threshold_amount:
                collector.is_frozen = True
                collector.save()
