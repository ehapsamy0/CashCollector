from rest_framework import serializers

from cash_collector.transaction.services import collect_amount
from cash_collector.transaction.services import deliver_amount

from .models import Transaction


class CollectAmountSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        task_id = validated_data.get("task_id")
        amount = validated_data.get("amount")
        transaction = collect_amount(task_id, amount)
        return transaction


class DeliverAmountSerializer(serializers.Serializer):
    collector_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        request = self.context["request"]
        collector_id = request.user.id
        amount = validated_data.get("amount")
        return deliver_amount(collector_id, amount)
