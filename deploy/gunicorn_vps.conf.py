# VPS only — systemd: gunicorn -c deploy/gunicorn_vps.conf.py
# На Render цей файл НЕ використовується (немає gunicorn.conf.py в корені).
import os

bind = os.environ.get("GUNICORN_BIND", "127.0.0.1:8000")
workers = int(os.environ.get("WEB_CONCURRENCY", "4"))
worker_class = "sync"
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True

_log_dir = os.environ.get("GUNICORN_LOG_DIR", "/var/log/kylymy")
accesslog = os.path.join(_log_dir, "gunicorn-access.log")
errorlog = os.path.join(_log_dir, "gunicorn-error.log")
loglevel = "info"
