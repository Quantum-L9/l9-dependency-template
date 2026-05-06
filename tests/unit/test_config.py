"""Unit tests for TemplateConfig and get_template_config."""
from __future__ import annotations

import pytest

from constellation_template.config import TemplateConfig, get_template_config


def test_safe_defaults_no_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """get_template_config() must not raise with no env vars set."""
    monkeypatch.delenv("L9_TEMPLATE_ENABLED", raising=False)
    config = get_template_config()
    assert config.enabled is True


def test_kill_switch_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    """L9_TEMPLATE_ENABLED=false must disable the capability."""
    get_template_config.cache_clear()
    monkeypatch.setenv("L9_TEMPLATE_ENABLED", "false")
    config = get_template_config()
    assert config.enabled is False


def test_kill_switch_true_variants(monkeypatch: pytest.MonkeyPatch) -> None:
    """pydantic-settings accepts standard truthy env var values."""
    for truthy in ("1", "true", "yes", "on", "True", "YES"):
        get_template_config.cache_clear()
        monkeypatch.setenv("L9_TEMPLATE_ENABLED", truthy)
        config = get_template_config()
        assert config.enabled is True, f"expected enabled=True for value {truthy!r}"


def test_config_is_frozen() -> None:
    config = TemplateConfig()
    with pytest.raises(Exception):  # noqa: B017
        config.enabled = False  # type: ignore[misc]


def test_config_rejects_extra_fields() -> None:
    with pytest.raises(Exception):  # noqa: B017
        TemplateConfig(enabled=True, unknown_field="boom")  # type: ignore[call-arg]


def test_validate_safe_ok() -> None:
    config = TemplateConfig(enabled=True)
    assert config.validate_safe() == []


def test_validate_safe_disabled() -> None:
    config = TemplateConfig(enabled=False)
    warnings = config.validate_safe()
    assert len(warnings) == 1
    assert "disabled" in warnings[0]
