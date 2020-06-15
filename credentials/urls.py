from django.urls import path

from . import views

app_name = "credentials"
urlpatterns = [
    path("", views.CredentialListView.as_view(), name="list"),
    path("add/", views.CredentialCreateView.as_view(), name="add"),
]
