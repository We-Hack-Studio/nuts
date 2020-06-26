from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.proxies.factory import exchange_proxy_factory
from credentials.models import Credential

from .models import Asset


@receiver(post_save, sender=Credential)
def init_assets(sender, instance: Credential, created=False, **kwargs):
    if created:
        exchange_proxy = exchange_proxy_factory(
            exchange_code=instance.exchange.code, test_net=instance.test_net
        )
        exchange_proxy.auth({"api_key": instance.api_key, "secret": instance.secret})
        balance = exchange_proxy.fetch_balance()
        asset_objs = []
        for currency in settings.ASSET_CURRENCY_LIST:
            principal = balance[currency]["total"]
            asset = Asset(
                currency=currency,
                principal=principal,
                balance=principal,
                credential=instance,
            )
            asset_objs.append(asset)

        Asset.objects.bulk_create(asset_objs)
