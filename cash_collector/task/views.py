import json

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from cash_collector.task.serializers import TaskReadeSerializer
from cash_collector.task.serializers import TaskWriteSerializer

from .models import Task

# Create your views here.


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskWriteSerializer

    def get_queryset(self):
        return Task.objects.filter(
            cash_collector=self.request.user.id, status=Task.Status.COLLECTED
        ).select_related("cash_collector")

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TaskReadeSerializer
        return TaskWriteSerializer


class NextTaskAPIView(APIView):
    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TaskReadeSerializer
        return TaskWriteSerializer

    def get(self, request):
        next_task = (
            Task.objects.filter(
                cash_collector=self.request.user.id, status=Task.Status.PENDING
            )
            .order_by("amount_due_at")
            .select_related("cash_collector")
            .first()
        )
        if next_task:
            serializer = self.get_serializer_class()
            return Response(serializer(next_task).data)
        raise ValidationError(_("task_error_message_to_no_next_task_for_you"))
