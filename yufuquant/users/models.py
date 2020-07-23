import os

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from core.validators import FileValidator

from .avatar_generator import AvatarGenerator


def user_avatar_path(instance, filename):
    return os.path.join("users", "avatars", instance.username, filename)


class User(AbstractUser):
    AVATAR_MAX_SIZE = 2 * 1024 * 1024
    AVATAR_ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
    AVATAR_DEFAULT_FILENAME = "default.jpeg"

    nickname = models.CharField(_("nickname"), max_length=30, blank=True)
    avatar = models.ImageField(
        _("avatar"),
        upload_to=user_avatar_path,
        validators=[
            FileValidator(
                max_size=AVATAR_MAX_SIZE, allowed_extensions=AVATAR_ALLOWED_EXTENSIONS
            )
        ],
        blank=True,
    )
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(70, 70)],
        format="jpeg",
        options={"quality": 90},
    )

    class Meta(AbstractUser.Meta):
        pass

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.nickname:
                self.nickname = self.username

            if not self.avatar:
                self.set_default_avatar()
        super(User, self).save(*args, **kwargs)

    def set_default_avatar(self):
        avatar_byte_array = AvatarGenerator.generate(self.username)
        self.avatar.save(
            self.AVATAR_DEFAULT_FILENAME, ContentFile(avatar_byte_array), save=False,
        )
