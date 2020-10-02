from .common import *

SECRET_KEY = "fake-local-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    "rest_framework.authentication.TokenAuthentication",
    # For browserable API when develop.
    # Must behind TokenAuthentication, otherwise unauthorized request will response 403 instead of 401.
    "rest_framework.authentication.SessionAuthentication",
]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL", "sqlite:///yufuquant/database/db.sqlite3")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
