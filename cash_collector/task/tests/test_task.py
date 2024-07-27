import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
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
    TaskFactory.create_batch(5, cash_collector=cash_collector)

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
        5, cash_collector=cash_collector, status=Task.Status.COLLECTED
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


