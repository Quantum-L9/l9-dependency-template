"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [tracing, observability, opentelemetry]
owner: platform-team
status: active
--- /L9_META ---
"""
from __future__ import annotations
import asyncio
import functools
from collections.abc import Callable
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

try:
    from opentelemetry import trace as _otel_trace
    _tracer = _otel_trace.get_tracer("constellation_template")
    _OTEL_AVAILABLE = True
except ImportError:
    _OTEL_AVAILABLE = False


def traced(span_name: str) -> Callable[[_F], _F]:
    """Wrap a sync or async function in an OTel span. No-op without opentelemetry-api."""
    def decorator(fn: _F) -> _F:
        if not _OTEL_AVAILABLE:
            return fn
        if asyncio.iscoroutinefunction(fn):
            @functools.wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                with _tracer.start_as_current_span(span_name):  # type: ignore[union-attr]
                    return await fn(*args, **kwargs)
            return async_wrapper  # type: ignore[return-value]

        @functools.wraps(fn)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            with _tracer.start_as_current_span(span_name):  # type: ignore[union-attr]
                return fn(*args, **kwargs)
        return sync_wrapper  # type: ignore[return-value]

    return decorator
