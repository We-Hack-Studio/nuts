import random
from datetime import timedelta

from django.utils import timezone
from robots.models import AssetRecord, AssetRecordSnap


def run():
    snap_objs = []
    asset_record_objs = []
    for asset_record in AssetRecord.objects.all():
        asset_record.total_principal = random.randint(10, 15)
        asset_record.total_balance = random.randint(15, 20)
        asset_record.total_principal_24h_ago = random.randint(10, 15)
        asset_record.total_balance_24h_ago = random.randint(15, 20)
        asset_record_objs.append(asset_record)

        now = timezone.now().replace(minute=0, second=0, microsecond=0)
        for i in range(100):
            dt = now - timedelta(hours=i)
            snap = AssetRecordSnap(
                asset_record=asset_record,
                total_principal=asset_record.total_principal,
                total_balance=random.randint(15, 20),
                period=AssetRecordSnap.PERIOD.h1,
                created_at=dt,
                modified_at=dt,
            )
            snap_objs.append(snap)

        now = now.replace(hour=12)
        for i in range(10):
            dt = now - timedelta(days=i)
            snap = AssetRecordSnap(
                asset_record=asset_record,
                total_principal=asset_record.total_principal,
                total_balance=random.randint(15, 20),
                period=AssetRecordSnap.PERIOD.d1,
                created_at=dt,
                modified_at=dt,
            )
            snap_objs.append(snap)

    AssetRecordSnap.objects.bulk_create(snap_objs, batch_size=1000)
    AssetRecord.objects.bulk_update(
        asset_record_objs,
        fields=[
            "total_principal",
            "total_balance",
            "total_principal_24h_ago",
            "total_balance_24h_ago",
        ],
        batch_size=1000,
    )
