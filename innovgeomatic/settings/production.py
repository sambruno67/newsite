from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.environ.get("SECRET_KEY", "changez-moi")

# ← Remplace tout le bloc DATABASES par ceci :
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
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

# ── Sécurité HTTPS ─────────────────────────────────────────
SECURE_SSL_REDIRECT             = True
SECURE_PROXY_SSL_HEADER         = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_BROWSER_XSS_FILTER       = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
X_FRAME_OPTIONS                 = "DENY"
SECURE_HSTS_SECONDS             = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_PRELOAD             = True