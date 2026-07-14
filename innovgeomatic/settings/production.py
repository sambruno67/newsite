from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.environ.get("SECRET_KEY", "changez-moi")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE"),
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("PGPASSWORD"),
        "HOST": os.environ.get("PGHOST"),
        "PORT": os.environ.get("PGPORT", "5432"),
    }
}

MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"

CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://innovgeomatic.com",
]

WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAIL_BASE_URL", "https://innovgeomatic.com")