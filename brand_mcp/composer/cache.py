"""TTL cache wrapper used by asset/Graph lookups."""
from __future__ import annotations

from typing import Any, Optional
from cachetools import TTLCache


class Cache:
    """Thin wrapper around cachetools.TTLCache with a friendlier API."""

    def __init__(self, ttl_seconds: int, maxsize: int = 512) -> None:
        self._c: TTLCache[str, Any] = TTLCache(maxsize=maxsize, ttl=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        return self._c.get(key)

    def set(self, key: str, value: Any) -> None:
        self._c[key] = value

    def clear(self) -> None:
        self._c.clear()
