from django.urls import path

from .. import views

urlpatterns = [
    path("login/", views.TokenCreateView.as_view(), name="login"),
    path("logout/", views.TokenDestroyView.as_view(), name="logout"),
]