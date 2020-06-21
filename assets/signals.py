from django.db.models.signals import post_save
from django.dispatch import receiver

from credentials.models import Credential
from django.conf import settings
from .models import Asset


@receiver(post_save, sender=Credential)
def init_assets(sender, instance: Credential, created=False, **kwargs):
    if created:
        asset_objs = []
        for currency in settings.ASSET_CURRENCY_LIST:
            asset = Asset(currency=currency, credential=instance)
            asset_objs.append(asset)

        Asset.objects.bulk_create(asset_objs)
