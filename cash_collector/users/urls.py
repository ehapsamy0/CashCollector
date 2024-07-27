from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from cash_collector.users.views import CashCollectorListView
from cash_collector.users.views import CashCollectorStatusView
from cash_collector.users.views import CustomTokenObtainPairView
from cash_collector.users.views import StatusAtTimeView

app_name = "users"
urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="obtain_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify_token"),
    path("status/", CashCollectorStatusView.as_view(), name="collector-status"),
    path("status-at-time/", StatusAtTimeView.as_view(), name="status-at-time"),
    path("cashcollectors/", CashCollectorListView.as_view(), name="cashcollector-list"),
]

