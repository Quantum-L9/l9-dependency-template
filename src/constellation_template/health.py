"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [health, observability]
owner: platform-team
status: active
--- /L9_META ---

Health check surface for constellation_template.

Exposes health_check() and HealthResult for use by nodes, orchestrators,
and CLI --check commands. Never raises. Always returns a structured result.
Replace 'template' / 'Template' throughout when bootstrapping a new package.
"""
from __future__ import annotations

import constellation_template
from constellation_template.config import get_template_config


class HealthResult:
    """Immutable health snapshot for a constellation_* capability.

    Attributes:
        capability: PyPI package name (e.g. "constellation-template").
        version: Package __version__ string.
        enabled: Whether the capability kill-switch is on.
        status: "ok" | "disabled" | "degraded".
        warnings: List of non-fatal warning messages from validate_safe().
        details: Arbitrary key/value metadata safe to log (no secrets).
    """

    __slots__ = ("capability", "version", "enabled", "status", "warnings", "details")

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

    def __setattr__(self, name: str, value: object) -> None:  # type: ignore[override]
        msg = f"HealthResult is immutable — cannot set {name!r}"
        raise AttributeError(msg)

    def __repr__(self) -> str:
        return (
            f"HealthResult(capability={self.capability!r}, "
            f"version={self.version!r}, status={self.status!r})"
        )

    def is_ok(self) -> bool:
        """Return True only when status is 'ok'."""
        return self.status == "ok"


def health_check() -> HealthResult:
    """Return a non-raising health snapshot for this capability.

    Safe to call at any time — catches all exceptions internally.
    Replace 'constellation-template' and the config import when bootstrapping.
    """
    try:
        cfg = get_template_config()
        warnings = cfg.validate_safe()
        status = "ok" if cfg.enabled and not warnings else (
            "disabled" if not cfg.enabled else "degraded"
        )
        return HealthResult(
            capability="constellation-template",
            version=constellation_template.__version__,
            enabled=cfg.enabled,
            status=status,
            warnings=warnings,
            details={"enabled": cfg.enabled},
        )
    except Exception as exc:  # noqa: BLE001
        return HealthResult(
            capability="constellation-template",
            version="unknown",
            enabled=False,
            status="degraded",
            warnings=[],
            details={"error": str(exc)},
        )
