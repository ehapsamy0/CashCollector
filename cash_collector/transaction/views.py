from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CollectAmountSerializer
from .serializers import DeliverAmountSerializer


class CollectAmountView(generics.CreateAPIView):
    serializer_class = CollectAmountSerializer


class DeliverAmountView(generics.CreateAPIView):
    serializer_class = DeliverAmountSerializer

