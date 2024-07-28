import json

from django.db import transaction
from django.db.models import Case
from django.db.models import IntegerField
from django.db.models import Value
from django.db.models import When
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from cash_collector.task.filters import TaskFilter
from cash_collector.task.serializers import TaskReadeSerializer
from cash_collector.task.serializers import TaskWriteSerializer
from cash_collector.users.permissions import IsNotFrozen

from .models import Task

# Create your views here.


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskWriteSerializer
    filterset_class = TaskFilter

    def get_queryset(self):
        filters = {}
        if self.request.user.manager:
            filters["cash_collector"] = self.request.user.id
            filters["status"] = Task.Status.COLLECTED
            return Task.objects.filter(**filters).select_related("cash_collector")
        return Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TaskReadeSerializer
        return TaskWriteSerializer


class NextTaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsNotFrozen]
    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TaskReadeSerializer
        return TaskWriteSerializer


    def get(self, request):
        now = timezone.now()
        next_task = (
            Task.objects.filter(
                cash_collector=self.request.user.id,
                status__in=[Task.Status.PENDING, Task.Status.PARTIALLY_COLLECTED],
                amount_due_at__lte=now,
            )
            .annotate(
                order=Case(
                    When(status=Task.Status.PARTIALLY_COLLECTED, then=Value(1)),
                    When(status=Task.Status.PENDING, then=Value(0)),
                    output_field=IntegerField(),
                )
            )
            .order_by("order", "amount_due_at")
            .select_related("cash_collector")
            .first()
        )
        if next_task:
            serializer = self.get_serializer_class()(next_task)
            return Response(serializer.data)
        raise ValidationError(_("task_error_message_to_no_next_task_for_you"))
