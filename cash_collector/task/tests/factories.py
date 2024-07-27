import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from cash_collector.task.models import Task
from cash_collector.users.models import User
from cash_collector.users.tests.factories import CashCollectorFactory


class TaskFactory(DjangoModelFactory):
    cash_collector = factory.SubFactory(CashCollectorFactory)
    customer_name = factory.Faker("name")
    address = factory.Faker("address")
    amount_due = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    amount_due_at = factory.LazyFunction(timezone.now)
    status = Task.Status.PENDING

    class Meta:
        model = Task
