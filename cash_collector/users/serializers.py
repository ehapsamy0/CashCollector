from rest_framework import serializers

from .models import CashCollector


class CashCollectorStatusSerializer(serializers.ModelSerializer):
    is_frozen = serializers.SerializerMethodField()

    class Meta:
        model = CashCollector
        fields = ["id", "username", "is_frozen","total_collected"]

    def get_is_frozen(self, obj):
        return obj.is_frozen


class StatusAtTimeSerializer(serializers.Serializer):
    collector_id = serializers.IntegerField()
    time_point = serializers.DateTimeField()
