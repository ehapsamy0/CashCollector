import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .factories import UserFactory

User = get_user_model()


@pytest.fixture()
def user(db):
    return User.objects.create_user(username="testuser", password="12345")  # noqa: S106

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
