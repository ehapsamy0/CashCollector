from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from cash_collector.core.utils import api_get_object_or_404
from cash_collector.users.permissions import IsManagerOrSelf
from cash_collector.users.serializers import CashCollectorStatusSerializer

from .models import CashCollector
from .models import Manager
from .models import User
from .serializers import StatusAtTimeSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    class CustomTokenObtainPairViewOutputSerializer(serializers.Serializer):
        refresh = serializers.CharField()
        access = serializers.CharField()

    class TokenSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user: User):
            token = super().get_token(user)

            # Users Claims
            token["name"] = user.name
            token["username"] = user.username
            return token

    serializer_class = TokenSerializer

    @extend_schema(
        request=TokenObtainPairSerializer,
        responses=CustomTokenObtainPairViewOutputSerializer,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CashCollectorStatusView(APIView):
    serializer_class = CashCollectorStatusSerializer

    def get(self, request):
        try:
            collector = CashCollector.objects.get(pk=request.user.id)
            return Response(self.serializer_class(collector).data)
        except CashCollector.DoesNotExist:
            msg = "CashCollector not found."
            raise NotFound(msg)  # noqa: B904


class StatusAtTimeView(APIView):
    serializer_class = StatusAtTimeSerializer

    def post(self, request):
        serializer = StatusAtTimeSerializer(data=request.data)
        if serializer.is_valid():
            collector_id = serializer.validated_data["collector_id"]
            time_point = serializer.validated_data["time_point"]
            collector = api_get_object_or_404(CashCollector, pk=collector_id)
            status = (
                "frozen" if collector.is_frozen_at(time_point) else "not frozen"
            )
            return Response({"status": status})
        raise ValidationError(serializer.errors)


class CashCollectorListView(generics.ListAPIView):
    serializer_class = CashCollectorStatusSerializer
    permission_classes = [IsManagerOrSelf]

    def get_queryset(self):
        user = self.request.user
        if user.manager:
            return CashCollector.objects.filter(id=user.id)
        return CashCollector.objects.filter(manager__isnull=False)

