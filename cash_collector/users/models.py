from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    """
    Default custom user model for cash_collector.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    USER_TYPE_CHOICES = [
        ("collector", "CashCollector"),
        ("manager", "Manager"),
    ]

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="collectors",
    )
    phone = models.CharField(max_length=255, default="", null=True, blank=True)  # noqa: DJ001
    image = models.URLField(default="", max_length=500, null=True, blank=True)  # noqa: DJ001
    total_collected = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def clean(self):
        if self.pk and self.collectors.exists() and self.manager is not None:
            msg = _(
                "users_error_message_to_say_a_user_with_collector_cannot_be_assigned_to_another_manager"
            )
            return ValidationError(msg)
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})




class CashCollector(User):
    class Meta:
        proxy = True

    @property
    def balance(self):
        return sum(
            transaction.amount
            for transaction in self.transactions.filter(transaction_type=1)
        ) - sum(
            transaction.amount
            for transaction in self.transactions.filter(transaction_type=2)
        )

    @property
    def is_frozen(self):
        threshold_balance = settings.MAX_BALANCE_THRESHOLD
        threshold_days = settings.FREEZE_DAYS_THRESHOLD
        if self.balance > threshold_balance:
            threshold_time = timezone.now() - timezone.timedelta(days=threshold_days)
            last_collection = (
                self.transactions.filter(transaction_type=1)
                .order_by("-timestamp")
                .first()
            )
            if last_collection and last_collection.timestamp < threshold_time:
                return True
        return False

    def is_frozen_at(self, time_point):
        threshold_balance = settings.MAX_BALANCE_THRESHOLD
        threshold_days = settings.FREEZE_DAYS_THRESHOLD
        transactions = self.transactions.filter(created_at__lte=time_point)
        balance = sum(
            transaction.amount
            for transaction in transactions.filter(transaction_type=1)
        ) - sum(
            transaction.amount
            for transaction in transactions.filter(transaction_type=2)
        )
        if balance > threshold_balance:
            threshold_time = time_point - timedelta(days=threshold_days)
            last_collection = (
                transactions.filter(transaction_type=1)
                .order_by("-created_at")
                .first()
            )
            if last_collection and last_collection.created_at < threshold_time:
                return True
        return False





class Manager(User):
    class Meta:
        proxy = True

    @property
    def collectors(self):
        return self.collectors.all()
