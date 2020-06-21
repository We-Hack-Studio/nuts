from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot

from .models import Position


@receiver(post_save, sender=Robot)
def init_position(sender, instance: Robot, created=False, **kwargs):
    if created:
        Position.objects.get_or_create(robot=instance)
