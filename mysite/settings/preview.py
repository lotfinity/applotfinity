"""Local ASUS preview settings, not for internet production deployment."""
import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import BASE_DIR


DEBUG = False
SECRET_KEY = os.environ.get("PORTFOLIO_PREVIEW_SECRET", "")
if not SECRET_KEY:
    raise ImproperlyConfigured("Set PORTFOLIO_PREVIEW_SECRET for the preview.")
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "192.168.1.110", "100.73.225.127"]
CSRF_TRUSTED_ORIGINS = [
    "http://192.168.1.110:8092", "http://100.73.225.127:8092"
]
WAGTAILADMIN_BASE_URL = "http://100.73.225.127:8092"
STATIC_ROOT = BASE_DIR / "preview_static"  # noqa: F405
WAGTAIL_CACHE = False

# Explicitly allow Django to serve uploaded media in the isolated local preview.
IS_LOCAL_PREVIEW = True
