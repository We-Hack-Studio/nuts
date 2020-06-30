from django.urls import path
from . import consumers

urlpatterns = [
    path("robots/<int:pk>/streams/", consumers.RobotStreamConsumer),
]
