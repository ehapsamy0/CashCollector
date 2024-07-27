import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .factories import CashCollectorFactory
from .factories import ManagerFactory
from .factories import UserFactory

User = get_user_model()



@pytest.fixture()
def collector(db):
    return CashCollectorFactory()


@pytest.fixture()
def manager1(db):
    return ManagerFactory()


@pytest.fixture()
def manager2(db):
    return ManagerFactory()




@pytest.mark.django_db()
def test_create_cash_collector(collector):
    assert collector.pk is not None
    assert collector.manager is None


@pytest.mark.django_db()
def test_create_manager(manager1):
    assert manager1.pk is not None
    assert manager1.manager is None


@pytest.mark.django_db()
def test_assign_cash_collector_to_manager(manager1):
    collector = CashCollectorFactory(manager=manager1)
    assert collector.manager == manager1


@pytest.mark.django_db()
def test_reassign_manager_with_collectors(manager1,manager2):
    collector = CashCollectorFactory(manager=manager1)
    assert collector.manager == manager1

    with pytest.raises(  # noqa: PT012
        ValidationError,
        match="users_error_message_to_say_a_user_with_collector_cannot_be_assigned_to_another_manager",
    ):
        manager1.manager = manager2
        manager1.save()
