# gunicorn.conf.py — конфігурація для production
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
accesslog = "/var/log/kylymy/gunicorn-access.log"
errorlog = "/var/log/kylymy/gunicorn-error.log"
loglevel = "info"
