import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.metrics import (
    API_REQUEST_DURATION_SECONDS,
    API_REQUESTS_TOTAL,
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/metrics"):
            return await call_next(request)

        start_time = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        API_REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()

        API_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

        return response