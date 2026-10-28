"""Production settings. Requires HTTPS and a server-generated secret.

Only enable DJANGO_TRUST_PROXY_SSL_HEADER when a trusted reverse proxy strips
and replaces X-Forwarded-Proto from untrusted clients.
"""
import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import BASE_DIR
from .base import DATABASES


DEBUG = False
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise ImproperlyConfigured("Set DJANGO_SECRET_KEY before starting production.")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", "hello-from.lotfinity.tech"
    ).split(",")
    if host.strip()
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS", "https://hello-from.lotfinity.tech"
    ).split(",")
    if origin.strip()
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
# Start with a modest HSTS policy. Increase only after HTTPS is verified.
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
DATABASES["default"]["NAME"] = os.environ.get(
    "DJANGO_DB_PATH", str(BASE_DIR / "db.sqlite3")
)
MEDIA_ROOT = os.environ.get("DJANGO_MEDIA_ROOT", str(BASE_DIR / "media"))
STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT", str(BASE_DIR / "static"))
# Wagtail's same-origin editor previews require framing within our own origin.
X_FRAME_OPTIONS = "SAMEORIGIN"

if os.environ.get("DJANGO_TRUST_PROXY_SSL_HEADER") == "1":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_FROM_EMAIL = "lotfinity <info@hello-from.lotfinity.tech>"
ADMINS = [("Administrator", "admin@hello-from.lotfinity.tech")]
MANAGERS = ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "cache",  # noqa: F405
        "KEY_PREFIX": "coderedcms",
        "TIMEOUT": 14400,
    }
}

# Content editors need immediate updates until site-setting cache invalidation is added.
WAGTAIL_CACHE = False
