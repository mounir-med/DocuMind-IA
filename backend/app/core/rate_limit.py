from collections import defaultdict, deque
from time import time

from fastapi import Request

from app.core.exceptions import AppError


class SlidingWindowLimiter:
    def __init__(self, max_calls: int, window_seconds: float) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time()
        bucket = self._hits[key]
        cutoff = now - self.window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        if len(bucket) >= self.max_calls:
            raise AppError("Trop de requêtes. Patientez quelques secondes.", status_code=429, code="rate_limited")
        bucket.append(now)


upload_limiter = SlidingWindowLimiter(max_calls=20, window_seconds=60)
chat_limiter = SlidingWindowLimiter(max_calls=30, window_seconds=60)


def client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"
