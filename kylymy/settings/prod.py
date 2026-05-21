import os
from urllib.parse import urlparse

from .base import *  # noqa: F401, F403

import sentry_sdk

DEBUG = False

# Render: ALLOWED_HOSTS / SITE_URL / CSRF з hostname сервісу (health check інакше 400)
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
if _render_host:
    _hosts = list(ALLOWED_HOSTS)  # noqa: F405
    if _render_host not in _hosts:
        ALLOWED_HOSTS = [*_hosts, _render_host]  # noqa: F405
    if SITE_URL in ("http://localhost", "http://localhost:8000", ""):  # noqa: F405
        SITE_URL = f"https://{_render_host}"  # noqa: F405

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "SAMEORIGIN"

# Render / reverse proxy (TLS завершується на edge)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF: обовʼязково вкажи повний origin(и) прод-сайту, напр. https://kylymy.onrender.com
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])  # noqa: F405
if not CSRF_TRUSTED_ORIGINS and SITE_URL:  # noqa: F405
    try:
        pr = urlparse(SITE_URL)  # noqa: F405
        if pr.scheme in ("https", "http") and pr.netloc:
            CSRF_TRUSTED_ORIGINS = [f"{pr.scheme}://{pr.netloc}"]
    except (TypeError, ValueError):
        pass

SENTRY_DSN = env("SENTRY_DSN", default="")  # noqa: F405
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )

# --- Статика (WhiteNoise) + медіа (локально або Cloudinary) ---
_WHITENOISE_STATICFILES = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}
_DISK_MEDIA = {
    "BACKEND": "django.core.files.storage.FileSystemStorage",
    "OPTIONS": {"location": str(MEDIA_ROOT)},  # noqa: F405
}

CLOUDINARY_URL = env("CLOUDINARY_URL", default="")  # noqa: F405
if CLOUDINARY_URL:
    _sf = INSTALLED_APPS.index("django.contrib.staticfiles")  # noqa: F405
    for _app in ("cloudinary_storage", "cloudinary"):
        if _app not in INSTALLED_APPS:  # noqa: F405
            INSTALLED_APPS.insert(_sf + 1, _app)  # noqa: F405
            _sf += 1
    STORAGES = {
        "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
        "staticfiles": _WHITENOISE_STATICFILES,
    }
else:
    STORAGES = {
        "default": _DISK_MEDIA,
        "staticfiles": _WHITENOISE_STATICFILES,
    }

# У Django 4.2+ пріоритет у STORAGES; прибираємо застарілий ключ з base
globals().pop("STATICFILES_STORAGE", None)
