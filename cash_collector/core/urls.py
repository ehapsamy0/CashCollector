from django.urls import include
from django.urls import path

app_name = "core"
urlpatterns = [
    path("users/", include("cash_collector.users.urls", namespace="tasks")),
    path("tasks/", include("cash_collector.task.urls", namespace="tasks")),
    path(
        "transactions/",
        include("cash_collector.transaction.urls", namespace="transactions"),
    ),
]
