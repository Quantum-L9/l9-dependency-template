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
    monkeypatch.setenv("L9_TEMPLATE_ENABLED", "false")
    # Direct construction bypasses lru_cache for this test
    from constellation_template.config import _env_bool
    enabled = _env_bool("L9_TEMPLATE_ENABLED", True)
    config = TemplateConfig(enabled=enabled)
    assert config.enabled is False


def test_kill_switch_true_variants(monkeypatch: pytest.MonkeyPatch) -> None:
    for truthy in ("1", "true", "yes", "on", "TRUE", "YES"):
        monkeypatch.setenv("L9_TEMPLATE_ENABLED", truthy)
        from constellation_template.config import _env_bool
        assert _env_bool("L9_TEMPLATE_ENABLED", False) is True


def test_config_is_frozen() -> None:
    config = TemplateConfig()
    with pytest.raises(Exception):  # noqa: B017
        config.enabled = False  # type: ignore[misc]


def test_config_rejects_extra_fields() -> None:
    with pytest.raises(Exception):  # noqa: B017
        TemplateConfig(enabled=True, unknown_field="boom")  # type: ignore[call-arg]
