"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [retry, resilience]
owner: platform-team
status: active
--- /L9_META ---
"""
from __future__ import annotations
import functools
from collections.abc import Callable
from typing import Any, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
    _TENACITY_AVAILABLE = True
except ImportError:
    _TENACITY_AVAILABLE = False


def with_retry(
    *, max_attempts: int = 3, wait_min: float = 1.0,
    wait_max: float = 10.0, reraise: bool = True,
) -> Callable[[_F], _F]:
    """Decorator factory for retrying with exponential back-off.

    No-op (single attempt, immediate reraise) when tenacity is not installed.
    """
    if _TENACITY_AVAILABLE:
        return retry(  # type: ignore[return-value]
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(min=wait_min, max=wait_max),
            reraise=reraise,
        )

    def no_op_decorator(fn: _F) -> _F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return fn(*args, **kwargs)
        return wrapper  # type: ignore[return-value]

    return no_op_decorator
