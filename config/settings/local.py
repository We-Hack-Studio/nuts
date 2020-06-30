from .common import *

SECRET_KEY = "fake-local-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
    }
}
