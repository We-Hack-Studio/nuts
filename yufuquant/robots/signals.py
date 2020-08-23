import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AssetRecord, Robot


@receiver(post_save, sender=Robot)
def init_asset_record(sender, instance: Robot, created: bool = False, **kwargs):
    if created:
        AssetRecord.objects.create(
            currency=instance.target_currency, robot=instance,
        )


@receiver(post_save, sender=Robot)
def init_strategy_parameters(sender, instance: Robot, created: bool = False, **kwargs):
    if created:
        parameter_spec = instance.strategy_template.parameter_spec
        parameters = {
            "version": parameter_spec["version"],
        }
        fields = {}
        for field in parameter_spec["fields"]:
            fields[field["code"]] = field["default"]
        parameters["fields"] = fields
        instance.strategy_parameters = parameters
        instance.save(update_fields=["strategy_parameters"])
