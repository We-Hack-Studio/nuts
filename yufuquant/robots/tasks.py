from datetime import timedelta

from celery import shared_task
from django.db.models import Prefetch
from django.utils import timezone

from .models import AssetRecord, AssetRecordSnap


def make_asset_record_snaps(period):
    h24_ago = timezone.now() + timedelta(minutes=30) - timedelta(hours=24)
    h24_ago = h24_ago.replace(minute=0, second=0, microsecond=0)
    h24_ago_start = h24_ago - timedelta(minutes=3)
    h24_ago_end = h24_ago + timedelta(minutes=3)
    # 只记录录入了本金和余额的资产
    asset_record_qs = (
        AssetRecord.objects.all()
        .filter(total_principal__gt=0, total_balance__gt=0)
        .prefetch_related(
            Prefetch(
                "snaps",
                queryset=AssetRecordSnap.objects.filter(
                    created_at__gt=h24_ago_start,
                    created_at__lt=h24_ago_end,
                    period=period,
                ).order_by("-created_at"),
                to_attr="prefetched_snaps",
            )
        )
    )
    asset_record_objs = []
    snap_objs = []
    for asset_record in asset_record_qs:
        snap = AssetRecordSnap(
            total_principal=asset_record.total_principal,
            total_balance=asset_record.total_balance,
            period=period,
            asset_record=asset_record,
        )
        snap_objs.append(snap)
        if len(asset_record.prefetched_snaps) > 0:
            snap_24h_ago = asset_record.prefetched_snaps[0]
            asset_record.total_principal_24h_ago = snap_24h_ago.total_principal
            asset_record.total_balance_24h_ago = snap_24h_ago.total_balance
            asset_record_objs.append(asset_record)

    AssetRecordSnap.objects.bulk_create(snap_objs, batch_size=1000)
    if len(asset_record_objs) > 0:
        AssetRecord.objects.bulk_update(
            asset_record_objs,
            fields=["total_balance_24h_ago", "total_principal_24h_ago"],
            batch_size=1000,
        )


@shared_task
def make_asset_record_snaps_task(period):
    make_asset_record_snaps(period)
