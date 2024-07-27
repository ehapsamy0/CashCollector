from django.utils import timezone
from rest_framework.exceptions import ValidationError

from cash_collector.core.utils import api_get_object_or_404
from cash_collector.task.models import Task
from cash_collector.users.models import CashCollector

from .models import Transaction


def collect_amount(task_id, amount):
    try:
        task = api_get_object_or_404(Task, id=task_id, status=Task.Status.PENDING)
        collector = task.cash_collector

        # Create a transaction for the collected amount
        collector.total_collected += amount
        collector.save()
        transaction = Transaction.objects.create(
            cash_collector=collector,
            amount=amount,
            transaction_type=1,
            task=task,
        )

        # Update task status to collected
        task.status = Task.Status.COLLECTED
        task.save()

        # Update collector's last collection time
        collector.last_collection_time = timezone.now()
        collector.save()

        return transaction  # noqa: TRY300
    except Task.DoesNotExist:
        msg = "Task not found or already completed"
        raise ValueError(msg)  # noqa: B904


def deliver_amount(collector_id, amount):
    try:
        collector = api_get_object_or_404(CashCollector, pk=collector_id)

        # Ensure the collector has enough balance to deliver
        if collector.total_collected < amount:
            msg = "Insufficient balance to deliver"
            raise ValidationError(msg)

        manager = collector.manager
        if not manager:
            msg = "Collector does not have an assigned manager"
            raise ValidationError(msg)

        # Update collector's and manager's total collected
        collector.total_collected -= amount
        manager.total_collected += amount
        collector.save()
        manager.save()

        # Create a transaction for the delivered amount
        transaction = Transaction.objects.create(
            cash_collector=collector, amount=amount, transaction_type=2,
        )

        # Update collector's balance and last delivery time
        collector.last_delivery_time = timezone.now()
        collector.is_frozen = False
        collector.save()

        return transaction  # noqa: TRY300
    except CashCollector.DoesNotExist:
        msg = "CashCollector not found"
        raise ValueError(msg)  # noqa: B904
