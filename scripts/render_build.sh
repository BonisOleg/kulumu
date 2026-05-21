#!/usr/bin/env bash
# Збірка на Render (Native Python). Викликається як buildCommand.
set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-kylymy.settings.prod}"

python -m pip install --upgrade pip
pip install -r requirements/prod.txt

python manage.py collectstatic --noinput

if [ -n "${DATABASE_URL:-}" ]; then
  python manage.py migrate --noinput
fi
