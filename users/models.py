from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField("昵称", max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username
        super(User, self).save(*args, **kwargs)
