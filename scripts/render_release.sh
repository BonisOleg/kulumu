#!/usr/bin/env bash
# Опційна фаза після деплою: міграції. У Render додай як «Post-Deploy Command» або запускай вручну один раз.
set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-kylymy.settings.prod}"

python manage.py migrate --noinput
