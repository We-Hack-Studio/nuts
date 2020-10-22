import json

from django.core.management.base import BaseCommand
from django.db import transaction
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
from robots.models import AssetRecordSnap
from robots.tasks import make_asset_record_snaps_task


class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - {make_asset_record_snaps_task.name}
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print("Deleting all periodic tasks and schedules...\n")

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                "task": make_asset_record_snaps_task,
                "name": "Make robot asset record snaps every day",
                # https://crontab.guru/every-day-at-midnight
                "cron": {
                    "minute": "0",
                    "hour": "0",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
                "enabled": True,
                "args": json.dumps([AssetRecordSnap.PERIOD.d1]),
            },
            {
                "task": make_asset_record_snaps_task,
                "name": "Make robot asset record snaps every hour",
                # https://crontab.guru/every-1-hour
                "cron": {
                    "minute": "0",
                    "hour": "*",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
                "enabled": True,
                "args": json.dumps([AssetRecordSnap.PERIOD.h1]),
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(**periodic_task["cron"])

            PeriodicTask.objects.create(
                name=periodic_task["name"],
                task=periodic_task["task"].name,
                crontab=cron,
                enabled=periodic_task["enabled"],
                args=periodic_task.get("args", "[]"),
            )
