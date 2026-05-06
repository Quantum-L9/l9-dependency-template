"""Unit tests for TemplateConfig, get_template_config, and config schema."""
from __future__ import annotations
import pytest
from constellation_template.config import TemplateConfig, get_template_config

def test_safe_defaults_no_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("L9_TEMPLATE_ENABLED", raising=False)
    assert get_template_config().enabled is True

def test_kill_switch_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    get_template_config.cache_clear()
    monkeypatch.setenv("L9_TEMPLATE_ENABLED", "false")
    assert get_template_config().enabled is False

def test_kill_switch_true_variants(monkeypatch: pytest.MonkeyPatch) -> None:
    for truthy in ("1", "true", "yes", "on", "True", "YES"):
        get_template_config.cache_clear()
        monkeypatch.setenv("L9_TEMPLATE_ENABLED", truthy)
        assert get_template_config().enabled is True, f"expected True for {truthy!r}"

def test_config_is_frozen() -> None:
    with pytest.raises(Exception):
        TemplateConfig().enabled = False  # type: ignore[misc]

def test_config_rejects_extra_fields() -> None:
    with pytest.raises(Exception):
        TemplateConfig(unknown_field="boom")  # type: ignore[call-arg]

def test_validate_safe_ok() -> None:
    assert TemplateConfig(enabled=True).validate_safe() == []

def test_validate_safe_disabled() -> None:
    warnings = TemplateConfig(enabled=False).validate_safe()
    assert len(warnings) == 1
    assert "disabled" in warnings[0]

def test_singleton_returns_same_instance() -> None:
    get_template_config.cache_clear()
    assert get_template_config() is get_template_config()

def test_config_schema_contract() -> None:
    """P3.2: JSON schema snapshot contract — drift fails this test."""
    schema = TemplateConfig.model_json_schema()
    props = schema.get("properties", {})
    assert "enabled" in props
    assert props["enabled"].get("type") == "boolean"
    assert props["enabled"].get("default") is True
    assert schema.get("title") == "TemplateConfig"
