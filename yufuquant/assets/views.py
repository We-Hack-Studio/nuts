from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Asset
from .serializers import AssetSerializer


class AssetViewSet(
    mixins.UpdateModelMixin, viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = AssetSerializer
    lookup_value_regex = "[0-9]+"

    def get_queryset(self):
        user = self.request.user
        qs = Asset.objects.all()
        if user.is_superuser:
            return qs
        return qs.filter(credential__user=user)
