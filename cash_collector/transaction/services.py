from django.db import transaction as db_transaction
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

        if task.amount_due - task.amount_collected < amount:
            msg = "Cannot collect more than the amount due"
            raise ValueError(msg)
        # Start a database transaction
        with db_transaction.atomic():
            task.amount_collected += amount
            task.status = (
                Task.Status.PARTIALLY_COLLECTED
                if task.amount_collected < task.amount_due
                else Task.Status.COLLECTED
            )
            task.save()

            collector.total_collected += amount
            collector.save()
            return Transaction.objects.create(
                cash_collector=collector,
                amount=amount,
                transaction_type=Transaction.Type.COLLECT,
                task=task,
            )

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

        # Start a database transaction
        with db_transaction.atomic():
            collector.total_collected -= amount
            manager.total_collected += amount
            collector.save()
            manager.save()

            # Create a transaction for the delivered amount
            transaction = Transaction.objects.create(
                cash_collector=collector,
                amount=amount,
                transaction_type=Transaction.Type.DELIVER,
            )

            # Update collector's
            collector.is_frozen = False
            collector.save()

            return transaction
    except CashCollector.DoesNotExist:
        msg = "CashCollector not found"
        raise ValueError(msg)  # noqa: B904
