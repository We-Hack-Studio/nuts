from typing import Any

import credentials.views
import exchanges.views
import robots.views
import strategies.views
import users.views
from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_bulk.routes import BulkRouter

if settings.DEBUG:
    # Why type as Any?
    # See: https://mypy.readthedocs.io/en/stable/common_issues.html#redefinitions-with-incompatible-types
    router: Any = BulkRouter()
else:
    router = SimpleRouter()

router.register("users", users.views.UserViewSet, basename="user")
router.register("robots", robots.views.RobotViewSet, basename="robot")
router.register(
    "strategies",
    strategies.views.StrategyViewSet,
    basename="strategy",
)
router.register("exchanges", exchanges.views.ExchangeViewSet, basename="exchange")
router.register(
    "credentials", credentials.views.CredentialViewSet, basename="credential"
)

app_name = "api"
urlpatterns = router.urls + [path("auth/", include("users.urls.auth"))]
