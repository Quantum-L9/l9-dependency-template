"""Unit tests for configure_logging() and get_logger()."""
from __future__ import annotations
from constellation_template.logging import _State, configure_logging, get_logger

def _reset() -> None:
    _State.configured = False

def test_get_logger_returns_logger() -> None:
    assert get_logger("test") is not None

def test_get_logger_default_name() -> None:
    assert get_logger() is not None

def test_configure_logging_idempotent() -> None:
    _reset()
    configure_logging()
    assert _State.configured is True
    configure_logging()
    assert _State.configured is True
    _reset()

def test_configure_logging_json_mode() -> None:
    _reset()
    configure_logging(render_json=True)
    assert _State.configured is True
    _reset()

def test_configure_logging_console_mode() -> None:
    _reset()
    configure_logging(render_json=False)
    assert _State.configured is True
    _reset()
