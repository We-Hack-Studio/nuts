from django_filters import rest_framework as drf_filters

from .models import Grid


class GridFilter(drf_filters.FilterSet):
    class Meta:
        model = Grid
        fields = ["robot_id"]
