"""Local development settings; not suitable for public deployment."""
import os

from django.core.management.utils import get_random_secret_key

from .base import *  # noqa: F403


DEBUG = True
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or get_random_secret_key()
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]"
).split(",")
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
WAGTAIL_CACHE = False

# Only development gets interactive debug tooling.
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

try:
    from .local import *  # noqa: F403,F401
except ImportError:
    pass
