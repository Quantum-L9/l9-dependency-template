"""Integration smoke tests — validates scaffold wiring end-to-end."""
from __future__ import annotations

from pathlib import Path

import constellation_template
from constellation_template.config import get_template_config
from constellation_template.health import health_check


def test_package_importable() -> None:
    assert constellation_template.__version__


def test_health_check_returns_ok() -> None:
    result = health_check()
    assert result.status in {"ok", "disabled", "degraded"}
    assert result.capability == "constellation-template"


def test_config_survives_cache_clear() -> None:
    get_template_config.cache_clear()
    c1 = get_template_config()
    get_template_config.cache_clear()
    c2 = get_template_config()
    assert c1 == c2


def test_acceptance_gate_import() -> None:
    """ARCHITECTURE.md acceptance gate 2: import works with zero config."""
    from constellation_template import TemplateConfig, get_template_config  # noqa: F401
    assert TemplateConfig is not None


def test_acceptance_gate_safe_defaults() -> None:
    """ARCHITECTURE.md acceptance gate 3: factory returns safe defaults, never raises."""
    get_template_config.cache_clear()
    cfg = get_template_config()
    assert cfg.enabled is True
