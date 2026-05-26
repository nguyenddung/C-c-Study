"""
Structured request/response logger middleware.

Logs every HTTP request as a single JSON line with:
  method, path, status_code, duration_ms, client_ip

Uses structlog for structured output; integrates cleanly with any
log aggregation pipeline (Datadog, Loki, CloudWatch, etc.).
"""

import time

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger("cocstudy.http")


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """Log all requests at INFO level; 5xx responses at ERROR level."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()

        # Capture response
        response: Response = await call_next(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        client_ip = request.client.host if request.client else "unknown"

        log_fn = logger.error if response.status_code >= 500 else logger.info
        log_fn(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            client_ip=client_ip,
            user_agent=request.headers.get("user-agent", ""),
        )

        # Expose timing header for debugging
        response.headers["X-Response-Time"] = f"{duration_ms}ms"
        return response