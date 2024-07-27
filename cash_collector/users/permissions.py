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
