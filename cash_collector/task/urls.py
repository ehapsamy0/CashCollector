from django.urls import path

from .views import NextTaskAPIView
from .views import TaskListAPIView

app_name = "tasks"
urlpatterns = [
    path("", TaskListAPIView.as_view(), name="list-create"),
    path("next-task/", NextTaskAPIView.as_view(), name="next-task"),

]
