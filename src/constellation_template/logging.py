"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [logging, observability, structlog]
owner: platform-team
status: active
--- /L9_META ---

Canonical structured logging scaffold for constellation_* packages.
configure_logging() is opt-in. get_logger() is always safe at module level.
"""
from __future__ import annotations
import logging
import threading
import structlog


class _State:
    """Module-level singleton state via class body to avoid global mutation."""
    lock: threading.Lock = threading.Lock()
    configured: bool = False


def configure_logging(*, level: str = "INFO", render_json: bool = True) -> None:
    """Idempotent structlog setup. Safe to call multiple times; configures once.

    Must NOT be called at import time from library code.
    Call from application entry points (CLI main, node __main__, test conftest).
    """
    with _State.lock:
        if _State.configured:
            return
        logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))
        processors: list[structlog.types.Processor] = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.ExceptionRenderer(),
            structlog.processors.JSONRenderer() if render_json
            else structlog.dev.ConsoleRenderer(),
        ]
        structlog.configure(
            processors=processors,
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.INFO)
            ),
            cache_logger_on_first_use=True,
        )
        _State.configured = True


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a structlog BoundLogger. Safe at module level. Never auto-configures."""
    return structlog.get_logger(name or "constellation_template")
