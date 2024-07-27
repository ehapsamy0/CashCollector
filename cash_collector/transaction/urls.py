from django.urls import path

from .views import CollectAmountView
from .views import DeliverAmountView

app_name = "transactions"

urlpatterns = [
    # Other URL patterns
    path("collect/", CollectAmountView.as_view(), name="collect-amount"),
    path("pay/", DeliverAmountView.as_view(), name="deliver-amount"),
]
