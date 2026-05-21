#!/usr/bin/env bash
# Старт на Render: перевірка env, django check, gunicorn → stdout.
set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-kylymy.settings.prod}"

if [ -z "${SECRET_KEY:-}" ]; then
  echo "FATAL: SECRET_KEY is not set. Render → Environment → add SECRET_KEY."
  exit 1
fi

echo "==> Python: $(python --version 2>&1)"
echo "==> DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"
echo "==> RENDER_EXTERNAL_HOSTNAME=${RENDER_EXTERNAL_HOSTNAME:-<not set>}"

python manage.py check

_bind_port="${PORT:-10000}"

exec gunicorn kylymy.wsgi:application \
  --bind "0.0.0.0:${_bind_port}" \
  --workers 2 \
  --timeout 120 \
  --error-logfile - \
  --access-logfile - \
  --log-level info
