"""Unit tests for @traced decorator (sync and async, with and without otel)."""
from __future__ import annotations
import pytest
from constellation_template.tracing import _OTEL_AVAILABLE, traced

def test_traced_sync_return_value() -> None:
    @traced("test.op")
    def add(a: int, b: int) -> int:
        return a + b
    assert add(2, 3) == 5

def test_traced_preserves_name() -> None:
    @traced("test.name")
    def my_func() -> None: pass
    assert my_func.__name__ == "my_func"

def test_traced_propagates_exception() -> None:
    @traced("test.exc")
    def failing() -> None:
        msg = "deliberate"
        raise ValueError(msg)
    with pytest.raises(ValueError, match="deliberate"):
        failing()

async def test_traced_async_return_value() -> None:
    @traced("test.async_op")
    async def async_add(a: int, b: int) -> int:
        return a + b
    assert await async_add(2, 3) == 5

async def test_traced_async_propagates_exception() -> None:
    @traced("test.async_exc")
    async def async_failing() -> None:
        msg = "async deliberate"
        raise ValueError(msg)
    with pytest.raises(ValueError, match="async deliberate"):
        await async_failing()

def test_otel_available_flag_is_bool() -> None:
    assert isinstance(_OTEL_AVAILABLE, bool)
