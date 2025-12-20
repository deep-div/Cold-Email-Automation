from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request
from fastapi.responses import Response
import time

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
    buckets=(0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5)
)

IN_PROGRESS_REQUESTS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress"
)

def setup_metrics(app):

    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        path = request.url.path
        method = request.method

        IN_PROGRESS_REQUESTS.inc()
        start_time = time.time()

        try:
            response = await call_next(request)
            status = response.status_code
            return response
        finally:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(method, path, status).inc()
            REQUEST_LATENCY.labels(method, path).observe(duration)
            IN_PROGRESS_REQUESTS.dec()

    @app.get("/metrics")
    async def metrics():
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
