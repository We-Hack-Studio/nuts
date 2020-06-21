from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_token(sender, instance=None, created=False, **kwargs):
    Token.objects.get_or_create(user=instance)
