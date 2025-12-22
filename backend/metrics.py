from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request
from fastapi.responses import Response
import time

REQUEST_COUNT = Counter(   # Counter always goes up
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(       # Histogram How values (like latency or size) are distributed across buckets
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
    buckets=(0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5)
)

IN_PROGRESS_REQUESTS = Gauge(   # Gauge can go up and down
    "http_requests_in_progress",
    "In-flight HTTP requests"
)

SERVER_ERRORS = Counter(
    "http_requests_5xx_total",
    "Total HTTP 5xx responses",
    ["method", "path"]
)


def setup_metrics(app):
    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        if request.url.path == "/metrics":       # Very IMportant otherwise it will cause 
            return await call_next(request) # Skip metrics for the metrics endpoint itself in my Fastapi app, this is collected after every few seconds in prometheus server yml file 

        method = request.method
        
        path = request.scope.get("path")      # records path which is /generate-email
        route_path = path if path else "unknown"

        IN_PROGRESS_REQUESTS.inc()
        start_time = time.time()
        status = "500"

        try:
            response = await call_next(request)
            status = str(response.status_code)
            return response
        except Exception:
            SERVER_ERRORS.labels(method, route_path).inc()
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(method, route_path, status).inc()
            REQUEST_LATENCY.labels(method, route_path).observe(duration)
            IN_PROGRESS_REQUESTS.dec()

            if status.startswith("5"):
                SERVER_ERRORS.labels(method, route_path).inc()

    @app.get("/metrics")
    async def metrics():
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
