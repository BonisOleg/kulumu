#!/usr/bin/env bash
# Збірка на Render (Native Python). Викликається як buildCommand.
set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-kylymy.settings.prod}"

python -m pip install --upgrade pip
pip install -r requirements/prod.txt

python manage.py collectstatic --noinput
_static_count="$(find staticfiles -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "==> collectstatic (build): ${_static_count} files in staticfiles/"
if [ "${_static_count}" -lt 50 ]; then
  echo "FATAL: collectstatic produced too few files"
  exit 1
fi

if [ -n "${DATABASE_URL:-}" ]; then
  python manage.py migrate --noinput
fi
