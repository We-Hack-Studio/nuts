from channels.routing import ProtocolTypeRouter, URLRouter
import streams.routing

application = ProtocolTypeRouter(
    {
        # Empty for now (http->django views is added by default)
        "websocket": URLRouter(
            streams.routing.websocket_urlpatterns
        ),
    }
)
