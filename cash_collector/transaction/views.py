from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cash_collector.users.permissions import IsNotFrozen

from .serializers import CollectAmountSerializer
from .serializers import DeliverAmountSerializer


class CollectAmountView(generics.CreateAPIView):
    serializer_class = CollectAmountSerializer
    permission_classes = [IsAuthenticated, IsNotFrozen]


class DeliverAmountView(generics.CreateAPIView):
    serializer_class = DeliverAmountSerializer

    permission_classes = [IsAuthenticated, IsNotFrozen]
