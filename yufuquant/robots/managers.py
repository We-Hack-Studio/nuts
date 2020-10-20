from django.db.models import Manager, QuerySet


class RobotQuerySet(QuerySet):
    pass


class RobotManager(Manager.from_queryset(RobotQuerySet)):  # type: ignore
    pass
