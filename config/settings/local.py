from .common import *

SECRET_KEY = "fake-local-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL", "sqlite:///database/db.sqlite3")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
