"""Integration smoke tests — validates scaffold wiring end-to-end."""
from __future__ import annotations
import constellation_template
from constellation_template.config import get_template_config
from constellation_template.health import health_check

def test_package_importable() -> None:
    assert constellation_template.__version__

def test_health_check_returns_valid_status() -> None:
    r = health_check()
    assert r.status in {"ok", "disabled", "degraded"}
    assert r.capability == "constellation-template"

def test_config_survives_cache_clear() -> None:
    get_template_config.cache_clear()
    c1 = get_template_config()
    get_template_config.cache_clear()
    c2 = get_template_config()
    assert c1 == c2

def test_safe_defaults_acceptance() -> None:
    get_template_config.cache_clear()
    cfg = get_template_config()
    assert cfg.enabled is True

def test_all_new_modules_importable() -> None:
    from constellation_template import (  # noqa: F401
        ErrorCode, HealthCheckable, Configurable,
        configure_logging, get_logger, traced, with_retry,
    )
