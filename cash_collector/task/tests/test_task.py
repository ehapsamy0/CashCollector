import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from cash_collector.task.models import Task
from cash_collector.users.tests.factories import CashCollectorFactory
from cash_collector.users.tests.factories import ManagerFactory

from .factories import TaskFactory


@pytest.fixture()
def collector(db):
    return CashCollectorFactory()


@pytest.fixture()
def manager(db):
    return ManagerFactory()


@pytest.mark.django_db()
def test_task_creation_without_manager():
    cash_collector = CashCollectorFactory(manager=None)
    with pytest.raises(  # noqa: PT012
        ValidationError,
        match="task_error_message_to_say_you_cannot_assign_this_task_to_this_user_because_they_do_not_have_a_manager",
    ):
        task = TaskFactory(cash_collector=cash_collector)
        task.full_clean()


@pytest.mark.django_db()
def test_task_creation_with_manager(manager):
    cash_collector = CashCollectorFactory(manager=manager)
    task = TaskFactory(cash_collector=cash_collector)
    assert task.status == Task.Status.PENDING
    assert task.cash_collector == cash_collector


@pytest.mark.django_db()
def test_next_task_api(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager)
    TaskFactory.create_batch(
        5,
        cash_collector=cash_collector,
        amount_due_at=timezone.now(),
    )

    client.force_authenticate(user=cash_collector)
    url = "/api/tasks/next-task/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "customer_name" in response.data
    assert "amount_due" in response.data


@pytest.mark.django_db()
def test_no_next_task_api(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager)
    TaskFactory.create_batch(
        5,
        cash_collector=cash_collector,
        amount_due_at=timezone.now() + timezone.timedelta(hours=1),
        status=Task.Status.PENDING,
    )
    client.force_authenticate(user=cash_collector)
    url = "/api/tasks/next-task/"
    response = client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "task_error_message_to_no_next_task_for_you"


@pytest.mark.django_db()
def test_get_list_of_done_tasks(manager):
    client = APIClient()
    cash_collector = CashCollectorFactory(manager=manager)

    # Create tasks with different statuses
    TaskFactory.create_batch(
        3, cash_collector=cash_collector, status=Task.Status.PENDING
    )
    TaskFactory.create_batch(
        5, cash_collector=cash_collector, status=Task.Status.COLLECTED
    )

    client.force_authenticate(user=cash_collector)
    url = "/api/tasks/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert (
        len(response.data["results"]) == 5  # noqa: PLR2004
    )  # Only tasks with COLLECTED status should be returned
    for task in response.data["results"]:
        assert task["status"] == "collected"


@pytest.mark.django_db()
def test_manager_can_access_all_tasks(manager):
    client = APIClient()
    collectors = CashCollectorFactory.create_batch(5, manager=manager)
    tasks = [TaskFactory(cash_collector=collector) for collector in collectors]

    client.force_authenticate(user=manager)
    url = "/api/tasks/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == len(tasks)


@pytest.mark.django_db()
def test_collector_can_only_access_their_own_tasks(manager):
    client = APIClient()
    collector1 = CashCollectorFactory(manager=manager)
    collector2 = CashCollectorFactory(manager=manager)
    TaskFactory.create_batch(5, cash_collector=collector1, status=Task.Status.COLLECTED)
    TaskFactory.create_batch(5, cash_collector=collector2, status=Task.Status.COLLECTED)

    client.force_authenticate(user=collector1)
    url = "/api/tasks/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 5
    for task in response.data["results"]:
        assert task["cash_collector"] == collector1.id


@pytest.mark.django_db()
def test_get_next_task_pending_first(manager):
    client = APIClient()
    collector = CashCollectorFactory(manager=manager)
    TaskFactory(
        cash_collector=collector,
        status=Task.Status.PENDING,
    )
    TaskFactory(
        cash_collector=collector,
        status=Task.Status.PARTIALLY_COLLECTED,
    )

    client.force_authenticate(user=collector)
    url = "/api/tasks/next-task/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "pending"


@pytest.mark.django_db()
def test_get_next_task_partially_collected(manager):
    client = APIClient()
    collector = CashCollectorFactory(manager=manager)
    TaskFactory(
        cash_collector=collector,
        status=Task.Status.PENDING,
        amount_due_at=timezone.now() + timezone.timedelta(minutes=10),
    )
    TaskFactory(
        cash_collector=collector,
        status=Task.Status.PARTIALLY_COLLECTED,
        amount_due_at=timezone.now(),
    )

    client.force_authenticate(user=collector)
    url = "/api/tasks/next-task/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "partially_collected"
