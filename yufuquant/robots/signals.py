from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AssetRecord, Robot


@receiver(post_save, sender=Robot)
def init_asset_record(sender, instance: Robot, created: bool = False, **kwargs):
    if created:
        AssetRecord.objects.create(
            currency=instance.target_currency,
            robot=instance,
        )


@receiver(post_save, sender=Robot)
def init_strategy_parameters(sender, instance: Robot, created: bool = False, **kwargs):
    if created:
        spec = instance.strategy.specification
        strategy_parameters = {}
        for parameter in spec["parameters"]:
            strategy_parameters[parameter["code"]] = parameter["default"]
        instance.strategy_parameters = strategy_parameters
        instance.save(update_fields=["strategy_parameters"])
