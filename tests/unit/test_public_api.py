"""Smoke tests — every symbol in __all__ must be importable."""
from __future__ import annotations
import constellation_template

def test_all_symbols_importable() -> None:
    for name in constellation_template.__all__:
        assert hasattr(constellation_template, name), f"missing: {name}"

def test_version_present() -> None:
    assert isinstance(constellation_template.__version__, str)
    assert constellation_template.__version__

def test_required_exports_present() -> None:
    required = {
        "TemplateConfig", "get_template_config",
        "TemplateError", "TemplateConfigError", "TemplateRuntimeError", "ErrorCode",
        "HealthResult", "health_check",
        "configure_logging", "get_logger",
        "HealthCheckable", "Configurable",
        "with_retry", "traced",
    }
    missing = required - set(constellation_template.__all__)
    assert not missing, f"missing from __all__: {missing}"
