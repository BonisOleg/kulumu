# gunicorn.conf.py — production (VPS через deploy/gunicorn-kylymy.service -c ...)
# Render: startCommand передає --bind; conf auto-load з CWD.
import os

bind = os.environ.get("GUNICORN_BIND", "127.0.0.1:8000")
workers = int(os.environ.get("WEB_CONCURRENCY", "4"))
worker_class = "sync"
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# "-" = stdout/stderr (Render, systemd journal). Файли — лише якщо каталог існує (VPS).
_log_dir = os.environ.get("GUNICORN_LOG_DIR", "")
if _log_dir and os.path.isdir(_log_dir):
    accesslog = os.path.join(_log_dir, "gunicorn-access.log")
    errorlog = os.path.join(_log_dir, "gunicorn-error.log")
else:
    accesslog = "-"
    errorlog = "-"

loglevel = "info"
