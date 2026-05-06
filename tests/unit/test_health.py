"""Unit tests for health_check() and HealthResult."""
from __future__ import annotations
import asyncio
import pytest
from constellation_template.health import HealthResult, health_check

def test_health_check_returns_result() -> None:
    assert isinstance(health_check(), HealthResult)

def test_health_check_status_ok() -> None:
    r = health_check()
    assert r.status == "ok"
    assert r.enabled is True
    assert r.is_ok() is True

def test_health_check_status_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    from constellation_template.config import get_template_config
    get_template_config.cache_clear()
    monkeypatch.setenv("L9_TEMPLATE_ENABLED", "false")
    r = health_check()
    assert r.status == "disabled"
    assert r.enabled is False
    assert r.is_ok() is False

def test_health_check_capability_name() -> None:
    assert health_check().capability == "constellation-template"

def test_health_check_version_present() -> None:
    assert isinstance(health_check().version, str)
    assert health_check().version != ""

def test_health_result_is_immutable() -> None:
    with pytest.raises(AttributeError):
        health_check().status = "hacked"  # type: ignore[misc]

def test_health_check_never_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    from constellation_template import config as cfg_module
    from constellation_template.config import get_template_config
    get_template_config.cache_clear()
    def broken():
        msg = "simulated failure"
        raise RuntimeError(msg)
    monkeypatch.setattr(cfg_module, "get_template_config", broken)
    r = health_check()
    assert r.status == "degraded"
    assert "error" in r.details

async def test_health_check_from_async() -> None:
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, health_check)
    assert r.capability == "constellation-template"
