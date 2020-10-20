from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/v1/streams/", consumers.StreamConsumer),
]
