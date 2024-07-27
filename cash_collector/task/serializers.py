from rest_framework import serializers

from cash_collector.users.serializers import CashCollectorStatusSerializer

from .models import Task


class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskReadeSerializer(TaskWriteSerializer):
    status = serializers.CharField(source="get_status_display")
    # cash_collector =
    class Meta(TaskWriteSerializer.Meta):
        pass

