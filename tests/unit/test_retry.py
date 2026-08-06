"""Unit tests for with_retry decorator."""

from __future__ import annotations

import pytest

from constellation_template.retry import _TENACITY_AVAILABLE, with_retry


def test_with_retry_returns_callable() -> None:
    assert callable(with_retry(max_attempts=2))


def test_with_retry_success() -> None:
    @with_retry(max_attempts=2)
    def ok() -> str:
        return "ok"

    assert ok() == "ok"


def test_with_retry_propagates_exception() -> None:
    calls: list[int] = []

    @with_retry(max_attempts=2, wait_min=0.0, wait_max=0.0)
    def always_fails() -> None:
        calls.append(1)
        msg = "always fails"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="always fails"):
        always_fails()

    if _TENACITY_AVAILABLE:
        assert len(calls) == 2
    else:
        assert len(calls) == 1


def test_with_retry_preserves_name() -> None:
    @with_retry()
    def my_func() -> None:
        pass

    assert my_func.__name__ == "my_func"


def test_tenacity_flag_is_bool() -> None:
    assert isinstance(_TENACITY_AVAILABLE, bool)
