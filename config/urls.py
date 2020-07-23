"""yufu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_bulk.routes import BulkRouter

import credentials.views
import exchanges.views
import robots.views
import strategies.views
import users.views
from core.views import IndexView

router = BulkRouter()
router.register("users", users.views.UserViewSet, basename="user")
router.register("robots", robots.views.RobotViewSet, basename="robot")
router.register(
    "strategy-templates",
    strategies.views.StrategyTemplateViewSet,
    basename="strategy-template",
)
router.register("exchanges", exchanges.views.ExchangeViewSet, basename="exchange")
router.register(
    "credentials", credentials.views.CredentialViewSet, basename="credential"
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("auth/", include("allauth.account.urls")),
    path("robots/", include("robots.urls")),
    path("credentials/", include("credentials.urls")),
    path("api/", include("rest_auth.urls")),
    path("api/", include(router.urls)),
]
