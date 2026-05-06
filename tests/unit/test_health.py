"""Unit tests for health_check() and HealthResult."""
from __future__ import annotations

import pytest

from constellation_template.health import HealthResult, health_check


def test_health_check_returns_result() -> None:
    result = health_check()
    assert isinstance(result, HealthResult)


def test_health_check_status_ok_when_enabled() -> None:
    result = health_check()
    assert result.status == "ok"
    assert result.enabled is True
    assert result.is_ok() is True


def test_health_check_status_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    from constellation_template.config import get_template_config
    get_template_config.cache_clear()
    monkeypatch.setenv("L9_TEMPLATE_ENABLED", "false")
    result = health_check()
    assert result.status == "disabled"
    assert result.enabled is False
    assert result.is_ok() is False


def test_health_check_capability_name() -> None:
    result = health_check()
    assert result.capability == "constellation-template"


def test_health_check_version_present() -> None:
    result = health_check()
    assert isinstance(result.version, str)
    assert result.version != ""


def test_health_result_is_immutable() -> None:
    result = health_check()
    with pytest.raises(AttributeError):
        result.status = "hacked"  # type: ignore[misc]


def test_health_check_never_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """health_check() must not raise even if config is broken."""
    from constellation_template import config as cfg_module
    original = cfg_module.get_template_config

    def broken() -> None:
        msg = "simulated config failure"
        raise RuntimeError(msg)

    monkeypatch.setattr(cfg_module, "get_template_config", broken)
    result = health_check()
    assert result.status == "degraded"
    assert "error" in result.details
