from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Robot, AssetRecord


@receiver(post_save, sender=Robot)
def init_asset_record(sender, instance: Robot, created=False, **kwargs):
    if created:
        AssetRecord.objects.create(
            currency=instance.target_currency, robot=instance,
        )


# @receiver(post_save, sender=Robot)
# def create_finance_record(sender, instance: Robot, created=False, **kwargs):
#     if created:
#         # Todo: extract parameters from strategy template
#         if instance.market_type == Robot.MARKET_TYPE.spots:
#             pull_base = pull_quote = False
#             try:
#                 base_asset = Asset.objects.get(
#                     currency=instance.base_currency, credential=instance.credential
#                 )
#             except Asset.DoesNotExist:
#                 base_asset = Asset(
#                     currency=instance.base_currency, credential=instance.credential
#                 )
#                 pull_base = True
#
#             try:
#                 quote_asset = Asset.objects.get(
#                     currency=instance.quote_currency, credential=instance.credential
#                 )
#             except Asset.DoesNotExist:
#                 quote_asset = Asset(
#                     currency=instance.quote_currency, credential=instance.credential
#                 )
#                 pull_quote = True
#
#             if instance.pull_assets:
#                 if pull_base or pull_quote:
#                     proxy = exchange_proxy_factory(
#                         exchange_code=instance.credential.exchange.code,
#                         pair=instance.pair,
#                         test_net=instance.credential.test_net,
#                         credential={
#                             "api_key": instance.credential.api_key,
#                             "secret": instance.credential.secret,
#                             "passphrase": instance.credential.passphrase,
#                         },
#                     )
#                     proxy.set_market_type(market_type=instance.market_type)
#                     result = proxy.fetch_balance()
#                     if pull_base:
#                         base_asset.principal = base_asset.balance = result[
#                             base_asset.currency
#                         ]["total"]
#                         base_asset.save(update_fields=["principal", "balance"])
#
#                     if pull_quote:
#                         quote_asset.principal = quote_asset.balance = result[
#                             quote_asset.currency
#                         ]["total"]
#                         quote_asset.save(update_fields=["principal", "balance"])
#
#             instance.base_asset = base_asset
#             instance.quote_asset = quote_asset
#             instance.save(update_fields=["base_asset", "quote_asset"])
#
#         if instance.market_type == Robot.MARKET_TYPE.futures:
#             try:
#                 margin_asset = Asset.objects.get(
#                     currency=instance.margin_currency, credential=instance.credential
#                 )
#             except Asset.DoesNotExist:
#                 margin_asset = Asset(
#                     currency=instance.margin_currency, credential=instance.credential
#                 )
#                 if instance.pull_assets:
#                     proxy = exchange_proxy_factory(
#                         exchange_code=instance.credential.exchange.code,
#                         pair=instance.pair,
#                         test_net=instance.credential.test_net,
#                         credential={
#                             "api_key": instance.credential.api_key,
#                             "secret": instance.credential.secret,
#                             "passphrase": instance.credential.passphrase,
#                         },
#                     )
#                     proxy.set_market_type(market_type=instance.market_type)
#                     result = proxy.fetch_balance()
#                     margin_asset.principal = margin_asset.balance = result[
#                         margin_asset.currency
#                     ]["total"]
#                     margin_asset.save(update_fields=["principal", "balance"])
#
#             instance.margin_asset = margin_asset
#             instance.save(update_fields=["margin_asset"])
