from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Position
from .serializers import PositionSerializer


class PositionViewSet(
    mixins.UpdateModelMixin, viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = PositionSerializer
    lookup_value_regex = "[0-9]+"

    def get_queryset(self):
        user = self.request.user
        qs = Position.objects.all()
        if user.is_superuser:
            return qs
        return qs.filter(robot__credential__user=user)
