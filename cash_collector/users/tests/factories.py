from collections.abc import Sequence
import string
from typing import Any

from factory import Faker
from factory import PostGenerationMethodCall
from factory import fuzzy
from factory.django import DjangoModelFactory

from cash_collector.users.models import CashCollector
from cash_collector.users.models import User


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")
    total_collected = 0
    password = fuzzy.FuzzyText(chars=string.ascii_lowercase)
    _password = PostGenerationMethodCall(
        method_name="set_password", raw_password="123456789++"
    )

    class Meta:
        model = User
        django_get_or_create = ["username"]


class CashCollectorFactory(UserFactory):
    class Meta:
        model = CashCollector


class ManagerFactory(UserFactory):
    manager = None
