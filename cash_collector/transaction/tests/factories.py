import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from cash_collector.task.models import Task
from cash_collector.task.tests.factories import TaskFactory
from cash_collector.transaction.models import Transaction
from cash_collector.users.models import CashCollector
from cash_collector.users.models import User
from cash_collector.users.tests.factories import CashCollectorFactory


class TransactionFactory(DjangoModelFactory):
    cash_collector = factory.SubFactory(CashCollectorFactory)
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    transaction_type = Transaction.Type.COLLECT
    task = factory.SubFactory(TaskFactory)

    class Meta:
        model = Transaction
