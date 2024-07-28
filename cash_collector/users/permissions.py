from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from cash_collector.users.models import Manager


class IsManagerOrSelf(BasePermission):
    """
    Custom permission to only allow managers to access all records,
    and cash collectors to access only their own records.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is a manager
        if isinstance(request.user, Manager):
            return True
        # Allow access if the user is accessing their own record
        return obj == request.user


class IsNotFrozen(BasePermission):
    message = _("task_error_message_to_no_next_task_for_you_because_you_are_frozen")

    def has_permission(self, request, view):
        if request.user.is_frozen:
            raise ValidationError(self.message)
        return True
