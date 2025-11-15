"""Pytest configuration for Django project."""

import os

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

if not settings.configured:
    django.setup()

# Desabilitar Silk durante testes para evitar queries extras
# Isso é feito removendo o middleware e app do Silk
if "silk" in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS = [app for app in settings.INSTALLED_APPS if app != "silk"]

if "silk.middleware.SilkyMiddleware" in settings.MIDDLEWARE:
    settings.MIDDLEWARE = [
        m for m in settings.MIDDLEWARE if m != "silk.middleware.SilkyMiddleware"
    ]
