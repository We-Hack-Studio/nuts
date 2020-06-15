from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from grids.models import Grid
from robots.serializers import RobotConfigSerializer

from .forms import RobotForm
from .models import Robot
from .serializers import RobotSerializer


class RobotListView(ListView):
    model = Robot
    ordering = "-ping_time"
    template_name = "robots/robot_list.html"


class RobotDetailView(DetailView):
    model = Robot
    ordering = "-ping_time"
    template_name = "robots/robot_detail.html"
    context_object_name = "robot"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        grid_list = Grid.objects.all().order_by("index")
        context["grid_list"] = grid_list
        return context


class RobotCreateView(CreateView):
    model = Robot
    form_class = RobotForm
    template_name = "robots/robot_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("robots:list")


class RobotViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = RobotSerializer

    def get_queryset(self):
        return Robot.objects.all().order_by("-ping_time")

    @action(
        methods=["GET"], detail=True, serializer_class=RobotConfigSerializer,
    )
    def config(self, request, *args, **kwargs):
        robot = self.get_object()
        serializer = self.get_serializer(instance=robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="logs")
    def send_log(self, request, *args, **kwargs):
        channel_layer = get_channel_layer()
        data = request.data
        robot_id = data["robot_id"]
        text = {
            "topic": "log",
            "robot_id": robot_id,
            "datetime": datetime.now().strftime("%H:%M:%S"),
            "data": {"msg": data["msg"]},
        }
        event = {
            "type": "robot.stream",
            "text": text,
        }
        group_name = f"robot.{robot_id}"
        async_to_sync(channel_layer.group_send)(
            group_name, event,
        )
        return Response({"detail": "ok"})
