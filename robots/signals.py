from django.db.models.signals import post_save
from django.dispatch import receiver

from credentials.models import Credential
from django.conf import settings
from .models import Robot
from core.utils import KeyHelper


@receiver(post_save, sender=Robot)
def init_stream_key(sender, instance: Robot, created=False, **kwargs):
    if created:
        data = {"robot_id": instance.pk}
        stream_key = KeyHelper.make_key(data=data)
        instance.stream_key = stream_key
        instance.save(update_fields=["stream_key"])
