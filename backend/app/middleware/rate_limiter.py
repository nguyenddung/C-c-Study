"""Simple in-process rate limiter middleware (Redis-backed in production)."""

import time
from collections import defaultdict, deque

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Sliding-window rate limiter.

    Tracks request timestamps per client IP.  In production, replace the
    in-memory store with Redis for multi-instance deployments.
    """

    def __init__(self, app, requests_per_minute: int = 60) -> None:
        super().__init__(app)
        self._limit = requests_per_minute
        self._window = 60.0
        # ip -> deque of timestamps
        self._store: dict[str, deque] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ("/health", "/"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()
        window_start = now - self._window

        bucket = self._store[client_ip]
        # Evict old timestamps
        while bucket and bucket[0] < window_start:
            bucket.popleft()

        if len(bucket) >= self._limit:
            return Response(
                content='{"detail": {"code": "RATE_LIMITED", "message": "Too many requests"}}',
                status_code=429,
                media_type="application/json",
            )

        bucket.append(now)
        return await call_next(request)