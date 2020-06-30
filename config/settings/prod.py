from .common import *

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CORS_ORIGIN_ALLOW_ALL = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(ROOT_DIR, "database", "db.sqlite3"),
    }
}
