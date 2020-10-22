from datetime import timedelta

import pytest
from django.utils import timezone
from freezegun import freeze_time
from robots.models import AssetRecordSnap, Robot
from robots.tasks import make_asset_record_snaps

from .factories import RobotFactory


@pytest.mark.django_db
@freeze_time("2020-10-14 12:00:00")
def test_make_asset_record_snaps_with_period_1h():
    robot1: Robot = RobotFactory()
    robot2: Robot = RobotFactory()
    robot3: Robot = RobotFactory()
    robot4: Robot = RobotFactory()
    now = timezone.now()

    robot1.asset_record.total_principal = 1
    robot1.asset_record.total_balance = 1.1
    robot1.asset_record.save()

    robot2.asset_record.total_principal = 2
    robot2.asset_record.total_balance = 2.2
    robot2.asset_record.save()

    robot3.asset_record.total_principal = 3
    robot3.asset_record.total_balance = 3.3
    robot3.asset_record.save()

    robot4.asset_record.total_principal = 0
    robot4.asset_record.total_balance = 0
    robot4.asset_record.save()

    # make 24 hours ago snap for robot1 and robot2
    AssetRecordSnap.objects.create(
        asset_record=robot1.asset_record,
        total_balance=0.11,
        total_principal=0.1,
        created_at=now - timedelta(hours=24),
        modified_at=now - timedelta(hours=24),
        period=AssetRecordSnap.PERIOD.h1,
    )
    AssetRecordSnap.objects.create(
        asset_record=robot2.asset_record,
        total_balance=0.22,
        total_principal=0.2,
        created_at=now - timedelta(hours=24),
        modified_at=now - timedelta(hours=24),
        period=AssetRecordSnap.PERIOD.h1,
    )

    make_asset_record_snaps(period=AssetRecordSnap.PERIOD.h1)

    robot1.refresh_from_db()
    robot2.refresh_from_db()
    robot3.refresh_from_db()
    robot4.refresh_from_db()

    assert robot1.asset_record.snaps.count() == 2
    assert robot1.asset_record.total_balance_24h_ago == 0.11
    assert robot1.asset_record.total_principal_24h_ago == 0.1
    last_snap = robot1.asset_record.snaps.order_by("-created_at").first()
    assert last_snap.total_balance == 1.1
    assert last_snap.total_principal == 1
    assert last_snap.period == AssetRecordSnap.PERIOD.h1

    assert robot2.asset_record.snaps.count() == 2
    assert robot2.asset_record.total_balance_24h_ago == 0.22
    assert robot2.asset_record.total_principal_24h_ago == 0.2
    last_snap = robot2.asset_record.snaps.order_by("-created_at").first()
    assert last_snap.total_balance == 2.2
    assert last_snap.total_principal == 2
    assert last_snap.period == AssetRecordSnap.PERIOD.h1

    assert robot3.asset_record.snaps.count() == 1
    last_snap = robot3.asset_record.snaps.order_by("-created_at").first()
    assert last_snap.total_balance == 3.3
    assert last_snap.total_principal == 3
    assert last_snap.period == AssetRecordSnap.PERIOD.h1

    assert robot4.asset_record.snaps.count() == 0


@pytest.mark.django_db
@freeze_time("2020-10-14 00:00:00")
def test_make_asset_record_snaps_with_period_1d():
    robot1: Robot = RobotFactory()
    robot2: Robot = RobotFactory()
    robot3: Robot = RobotFactory()
    now = timezone.now()

    robot1.asset_record.total_principal = 1
    robot1.asset_record.total_balance = 1.1
    robot1.asset_record.save()

    robot2.asset_record.total_principal = 2
    robot2.asset_record.total_balance = 2.2
    robot2.asset_record.save()

    robot3.asset_record.total_principal = 0
    robot3.asset_record.total_balance = 0
    robot3.asset_record.save()

    # make 24 hours ago snap for robot1 and robot2
    AssetRecordSnap.objects.create(
        asset_record=robot1.asset_record,
        total_balance=0.11,
        total_principal=0.1,
        created_at=now - timedelta(hours=24),
        modified_at=now - timedelta(hours=24),
        period=AssetRecordSnap.PERIOD.d1,
    )

    make_asset_record_snaps(period=AssetRecordSnap.PERIOD.d1)

    robot1.refresh_from_db()
    robot2.refresh_from_db()
    robot3.refresh_from_db()

    assert robot1.asset_record.snaps.count() == 2
    assert robot1.asset_record.total_balance_24h_ago == 0.11
    assert robot1.asset_record.total_principal_24h_ago == 0.1
    last_snap = robot1.asset_record.snaps.order_by("-created_at").first()
    assert last_snap.total_balance == 1.1
    assert last_snap.total_principal == 1
    assert last_snap.period == AssetRecordSnap.PERIOD.d1

    assert robot2.asset_record.snaps.count() == 1
    last_snap = robot2.asset_record.snaps.order_by("-created_at").first()
    assert last_snap.total_balance == 2.2
    assert last_snap.total_principal == 2
    assert last_snap.period == AssetRecordSnap.PERIOD.d1

    assert robot3.asset_record.snaps.count() == 0
