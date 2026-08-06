"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [public-api]
owner: platform-team
status: active
--- /L9_META ---
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("constellation-template")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

from constellation_template.config import TemplateConfig, get_template_config
from constellation_template.errors import (
    ErrorCode,
    TemplateConfigError,
    TemplateError,
    TemplateRuntimeError,
)
from constellation_template.health import HealthResult, health_check
from constellation_template.logging import configure_logging, get_logger
from constellation_template.protocols import Configurable, HealthCheckable
from constellation_template.retry import with_retry
from constellation_template.tracing import traced

__all__ = [
    "__version__",
    "TemplateConfig",
    "get_template_config",
    "ErrorCode",
    "TemplateConfigError",
    "TemplateError",
    "TemplateRuntimeError",
    "HealthResult",
    "health_check",
    "configure_logging",
    "get_logger",
    "Configurable",
    "HealthCheckable",
    "with_retry",
    "traced",
]
