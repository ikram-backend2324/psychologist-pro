"""Gunicorn settings tuned for a small (~512 MB) instance such as Render Free."""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "2"))
worker_class = "gthread"
# AI feedback calls are bounded by AI_TIMEOUT_SECONDS (default 25 s); keep a margin.
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 20
max_requests = 500
max_requests_jitter = 50
accesslog = "-"
forwarded_allow_ips = "*"
