"""Lightweight JSONL telemetry for the Solidigm brand MCP server.

Behavior:

- **Disabled by default.** Set ``BRAND_MCP_TELEMETRY_ENABLED=1`` in the env
  to turn it on.
- Writes one JSONL line per event to ``brand_mcp/telemetry/YYYY-MM-DD.jsonl``
  (rotated daily).
- Best-effort: any I/O failure is swallowed. Telemetry must never affect
  request handling.

Schema (one line = one JSON object)::

    {
      "ts":   "2026-04-24T12:34:56.789Z",
      "event": "tool_call",
      "name": "get_color",
      "ok":   true,
      "ms":   12,
      "meta": {"name": "Solidigm Purple"}
    }

The ``meta`` payload is small and never contains user-identifying data.

Aggregation lives in :func:`load_recent_events` and :func:`aggregate` —
consumed by the ``/api/stats`` route and the admin dashboard.
"""
from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional

log = logging.getLogger(__name__)

_ENV_FLAG = "BRAND_MCP_TELEMETRY_ENABLED"


def _enabled() -> bool:
    return os.environ.get(_ENV_FLAG, "").strip().lower() in {"1", "true", "yes", "on"}


def _telemetry_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))  # brand_mcp/utils
    base = os.path.dirname(here)                       # brand_mcp
    return os.path.join(base, "telemetry")


def _today_path() -> str:
    return os.path.join(_telemetry_dir(), datetime.now(timezone.utc).strftime("%Y-%m-%d") + ".jsonl")


def record(event: str, name: str, ok: bool = True, ms: int = 0, meta: Optional[Dict[str, Any]] = None) -> None:
    """Append a single telemetry event. Never raises."""
    if not _enabled():
        return
    try:
        os.makedirs(_telemetry_dir(), exist_ok=True)
        line = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "event": event,
            "name": name,
            "ok": ok,
            "ms": ms,
            "meta": meta or {},
        }
        with open(_today_path(), "a", encoding="utf-8") as f:
            f.write(json.dumps(line, separators=(",", ":")) + "\n")
    except Exception as exc:  # noqa: BLE001
        log.debug("telemetry write failed: %s", exc)


def instrument_tool(tool_name: str, fn: Callable[..., Any]) -> Callable[..., Any]:
    """Wrap a sync or async tool function so each call is recorded."""
    import asyncio

    if asyncio.iscoroutinefunction(fn):
        async def _async_wrapper(*args: Any, **kwargs: Any) -> Any:
            t0 = time.perf_counter()
            try:
                result = await fn(*args, **kwargs)
                record("tool_call", tool_name, ok=True, ms=int((time.perf_counter() - t0) * 1000), meta=_safe_meta(kwargs))
                return result
            except Exception as exc:
                record("tool_call", tool_name, ok=False, ms=int((time.perf_counter() - t0) * 1000), meta={"error": type(exc).__name__})
                raise
        _async_wrapper.__name__ = fn.__name__
        _async_wrapper.__doc__ = fn.__doc__
        return _async_wrapper

    def _sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        t0 = time.perf_counter()
        try:
            result = fn(*args, **kwargs)
            record("tool_call", tool_name, ok=True, ms=int((time.perf_counter() - t0) * 1000), meta=_safe_meta(kwargs))
            return result
        except Exception as exc:
            record("tool_call", tool_name, ok=False, ms=int((time.perf_counter() - t0) * 1000), meta={"error": type(exc).__name__})
            raise
    _sync_wrapper.__name__ = fn.__name__
    _sync_wrapper.__doc__ = fn.__doc__
    return _sync_wrapper


def _safe_meta(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Strip large or PII-ish payloads. Keep only short scalar args."""
    out: Dict[str, Any] = {}
    for k, v in kwargs.items():
        if v is None:
            continue
        if isinstance(v, (bool, int, float)):
            out[k] = v
        elif isinstance(v, str):
            out[k] = v[:64]
        # everything else (lists, dicts, content blobs) is dropped
    return out


def load_recent_events(days: int = 30) -> List[Dict[str, Any]]:
    """Read events from the last ``days`` daily files. Best-effort."""
    out: List[Dict[str, Any]] = []
    base = _telemetry_dir()
    if not os.path.isdir(base):
        return out
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for name in sorted(os.listdir(base)):
        if not name.endswith(".jsonl"):
            continue
        try:
            day = datetime.strptime(name[:-6], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if day < cutoff:
            continue
        try:
            with open(os.path.join(base, name), "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            continue
    return out


def aggregate(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Group events into the shape expected by the /admin/stats dashboard."""
    by_tool: Dict[str, Dict[str, Any]] = {}
    by_color: Dict[str, int] = {}
    total = 0
    errors = 0
    latency_sum = 0
    latency_count = 0

    for ev in events:
        if ev.get("event") != "tool_call":
            continue
        total += 1
        if not ev.get("ok", True):
            errors += 1
        ms = ev.get("ms") or 0
        if isinstance(ms, (int, float)) and ms >= 0:
            latency_sum += ms
            latency_count += 1
        name = ev.get("name") or "unknown"
        bucket = by_tool.setdefault(name, {"calls": 0, "errors": 0})
        bucket["calls"] += 1
        if not ev.get("ok", True):
            bucket["errors"] += 1
        if name == "get_color":
            color = (ev.get("meta") or {}).get("name")
            if isinstance(color, str) and color:
                by_color[color] = by_color.get(color, 0) + 1

    top_tools = sorted(
        ({"name": k, **v} for k, v in by_tool.items()),
        key=lambda r: r["calls"],
        reverse=True,
    )
    top_colors = sorted(
        ({"name": k, "calls": v} for k, v in by_color.items()),
        key=lambda r: r["calls"],
        reverse=True,
    )[:20]

    return {
        "enabled": _enabled(),
        "total_calls": total,
        "error_count": errors,
        "error_rate": (errors / total) if total else 0.0,
        "avg_latency_ms": (latency_sum // latency_count) if latency_count else 0,
        "top_tools": top_tools,
        "top_colors": top_colors,
    }
