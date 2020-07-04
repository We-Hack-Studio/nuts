from django.urls import path
from . import consumers

urlpatterns = [
    path("ws/robots/<int:pk>/streams/", consumers.RobotStreamConsumer),
]
