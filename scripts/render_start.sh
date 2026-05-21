#!/usr/bin/env bash
# Старт на Render: перевірка env, django setup, gunicorn → stdout.
set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-kylymy.settings.prod}"

if [ -z "${SECRET_KEY:-}" ]; then
  echo "FATAL: SECRET_KEY is not set. Render → Environment → add SECRET_KEY."
  exit 1
fi

echo "==> Python: $(python --version 2>&1)"
echo "==> DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"
echo "==> RENDER_EXTERNAL_HOSTNAME=${RENDER_EXTERNAL_HOSTNAME:-<not set>}"
echo "==> DATABASE_URL set: $([ -n "${DATABASE_URL:-}" ] && echo yes || echo no)"
echo "==> REDIS_URL set: $([ -n "${REDIS_URL:-}" ] && echo yes || echo no)"

# stderr → stdout, щоб Render Logs показували traceback (інакше лише echo видно)
echo "==> Django setup..."
if ! python -u -c "
import os, sys, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '${DJANGO_SETTINGS_MODULE}')
try:
    import django
    django.setup()
    from django.core.management import call_command
    call_command('check')
    print('==> Django check OK')
except Exception:
    traceback.print_exc(file=sys.stdout)
    sys.stdout.flush()
    sys.exit(1)
" 2>&1; then
  echo "FATAL: Django failed to start (see traceback above)"
  exit 1
fi

_bind_port="${PORT:-10000}"
echo "==> Starting gunicorn on 0.0.0.0:${_bind_port}"

exec gunicorn kylymy.wsgi:application \
  --bind "0.0.0.0:${_bind_port}" \
  --workers 2 \
  --timeout 120 \
  --error-logfile - \
  --access-logfile - \
  --log-level info
