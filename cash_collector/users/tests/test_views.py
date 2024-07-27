import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .factories import CashCollectorFactory, ManagerFactory, UserFactory

User = get_user_model()


@pytest.fixture()
def user(db):
    return User.objects.create_user(username="testuser", password="12345")  # noqa: S106



@pytest.fixture()
def manager(db):
    return ManagerFactory()


@pytest.mark.django_db()
def test_obtain_token(user):
    client = APIClient()
    response = client.post(
        "/api/users/token/", {"username": "testuser", "password": "12345"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

    access_token = response.data["access"]
    decoded_token = client.post("/api/users/token/verify/", {"token": access_token})
    assert decoded_token.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_manager_can_access_all_collectors(manager):
    client = APIClient()
    CashCollectorFactory.create_batch(5, manager=manager)

    client.force_authenticate(user=manager)
    url = "/api/users/cashcollectors/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    print("XXXXXXXXXXXXXXXXXXXXXXXXXX",len(response.data["results"]))
    assert len(response.data["results"]) == 5

@pytest.mark.django_db()
def test_collector_can_only_access_their_own_record(manager):
    client = APIClient()
    collector = CashCollectorFactory(manager=manager)
    client.force_authenticate(user=collector)
    url = "/api/users/cashcollectors/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["id"] == collector.id
