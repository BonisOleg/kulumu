import os

from django.core.wsgi import get_wsgi_application

# Render виставляє RENDER=1; локально залишаємо dev, якщо DJANGO_SETTINGS_MODULE не задано
_default = "kylymy.settings.prod" if os.environ.get("RENDER") else "kylymy.settings.dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", _default)

application = get_wsgi_application()
