"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [health, observability]
owner: platform-team
status: active
--- /L9_META ---
"""

from __future__ import annotations

import threading
from importlib.metadata import PackageNotFoundError, version

from constellation_template.config import get_template_config
from constellation_template.logging import get_logger

_log = get_logger(__name__)
_LOCK: threading.Lock = threading.Lock()

try:
    _VERSION: str = version("constellation-template")
except PackageNotFoundError:
    _VERSION = "0.0.0+unknown"


class HealthResult:
    """Immutable health snapshot for a constellation_* capability."""

    __slots__ = ("capability", "version", "enabled", "status", "warnings", "details")
    capability: str
    version: str
    enabled: bool
    status: str
    warnings: list[str]
    details: dict[str, object]

    def __init__(
        self,
        *,
        capability: str,
        version: str,
        enabled: bool,
        status: str,
        warnings: list[str],
        details: dict[str, object],
    ) -> None:
        object.__setattr__(self, "capability", capability)
        object.__setattr__(self, "version", version)
        object.__setattr__(self, "enabled", enabled)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "warnings", warnings)
        object.__setattr__(self, "details", details)

    def __setattr__(self, name: str, value: object) -> None:
        msg = f"HealthResult is immutable — cannot set {name!r}"
        raise AttributeError(msg)

    def __repr__(self) -> str:
        return (
            f"HealthResult(capability={self.capability!r}, "
            f"version={self.version!r}, status={self.status!r})"
        )

    def is_ok(self) -> bool:
        return self.status == "ok"


def health_check() -> HealthResult:
    """Return a non-raising health snapshot for this capability. Thread-safe."""
    with _LOCK:
        try:
            cfg = get_template_config()
            warnings = cfg.validate_safe()
            if not cfg.enabled:
                status = "disabled"
            elif warnings:
                status = "degraded"
            else:
                status = "ok"
            result = HealthResult(
                capability="constellation-template",
                version=_VERSION,
                enabled=cfg.enabled,
                status=status,
                warnings=warnings,
                details={"enabled": cfg.enabled},
            )
        except Exception as exc:  # noqa: BLE001
            _log.warning("health_check failed", error=str(exc))
            result = HealthResult(
                capability="constellation-template",
                version=_VERSION,
                enabled=False,
                status="degraded",
                warnings=[],
                details={"error": str(exc)},
            )
    return result
