from django.urls import path

from . import views

app_name = "robots"
urlpatterns = [
    path("", views.RobotListView.as_view(), name="list"),
    path("<int:pk>/", views.RobotDetailView.as_view(), name="detail"),
    path("add/", views.RobotCreateView.as_view(), name="add"),
]
