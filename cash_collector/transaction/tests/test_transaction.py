import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from cash_collector.task.models import Task
from cash_collector.task.tests.factories import TaskFactory
from cash_collector.transaction.models import Transaction
from cash_collector.users.tests.factories import CashCollectorFactory
from cash_collector.users.tests.factories import ManagerFactory


@pytest.fixture()
def collector(db):
    return CashCollectorFactory()


@pytest.fixture()
def manager(db):
    return ManagerFactory()


@pytest.mark.django_db()
def test_collect_amount(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager)
    task = TaskFactory(cash_collector=cash_collector, amount_due=100)

    client.force_authenticate(user=cash_collector)
    url = "/api/transactions/collect/"
    response = client.post(url, {"task_id": task.id, "amount": 100.00})

    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.filter(
        cash_collector=cash_collector,
        task=task,
        transaction_type=Transaction.Type.COLLECT,
    ).exists()

    task.refresh_from_db()
    assert task.status == Task.Status.COLLECTED


@pytest.mark.django_db()
def test_collect_amount_invalid_task(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager)

    client.force_authenticate(user=cash_collector)
    url = "/api/transactions/collect/"
    response = client.post(url, {"task_id": 999, "amount": 100.00})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_deliver_amount(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager, total_collected=200.00)

    client.force_authenticate(user=cash_collector)
    url = "/api/transactions/pay/"
    response = client.post(url, {"amount": 100.00})

    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.filter(
        cash_collector=cash_collector, transaction_type=Transaction.Type.DELIVER
    ).exists()

    cash_collector.refresh_from_db()
    manager.refresh_from_db()
    assert cash_collector.total_collected == 100.00
    assert manager.total_collected == 100.00


@pytest.mark.django_db()
def test_deliver_amount_insufficient_balance(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager, total_collected=50.00)

    client.force_authenticate(user=cash_collector)
    url = "/api/transactions/pay/"
    response = client.post(url, {"amount": 100.00})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "Insufficient balance to deliver"


@pytest.mark.django_db()
def test_deliver_amount_no_manager():
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=None, total_collected=200.00)

    client.force_authenticate(user=cash_collector)
    url = "/api/transactions/pay/"
    response = client.post(url, {"amount": 100.00})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "Collector does not have an assigned manager"


@pytest.mark.django_db()
def test_partial_collect_amount(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager)
    task = TaskFactory(cash_collector=cash_collector, amount_due=200)

    client.force_authenticate(user=cash_collector)
    url = "/api/transactions/collect/"
    response = client.post(url, {"task_id": task.id, "amount": 100.00})

    assert response.status_code == status.HTTP_201_CREATED
    task.refresh_from_db()
    assert task.amount_collected == 100.00  # noqa: PLR2004
    assert task.status == Task.Status.PARTIALLY_COLLECTED


@pytest.mark.django_db()
def test_collect_amount_when_frozen(manager):
    client = APIClient()
    frozen_collector = CashCollectorFactory(manager=manager,is_frozen=True)
    task = TaskFactory(cash_collector=frozen_collector, status=Task.Status.PENDING)

    client.force_authenticate(user=frozen_collector)
    url = "/api/transactions/collect/"
    data = {"task_id": task.id, "amount": 100.00}
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "task_error_message_to_no_next_task_for_you_because_you_are_frozen"
        in response.data["message"]
    )
