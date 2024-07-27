from datetime import timedelta
from django.conf import settings

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import CashCollector

User = get_user_model()



@shared_task
def check_and_freeze_cash_collectors():
    threshold_balance = settings.MAX_BALANCE_THRESHOLD
    threshold_days = settings.FREEZE_DAYS_THRESHOLD
    now = timezone.now()
    threshold_time = now - timedelta(days=threshold_days)

    collectors_to_freeze = CashCollector.objects.filter(
        total_collected__gte=threshold_balance, last_collection_time__lte=threshold_time
    )
    for collector in collectors_to_freeze:
        collector.is_frozen = True
        collector.save()
