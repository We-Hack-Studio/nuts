from django.urls import path
from . import consumers

urlpatterns = [
    path("api/robots/logs/xxxx", consumers.RobotLogConsumer),
]
