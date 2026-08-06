"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [protocols, typing, extensibility]
owner: platform-team
status: active
--- /L9_META ---
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from constellation_template.health import HealthResult


@runtime_checkable
class HealthCheckable(Protocol):
    """Any object that can report its own health state."""

    def check_health(self) -> HealthResult:
        """Return a non-raising health snapshot."""
        ...


@runtime_checkable
class Configurable(Protocol):
    """Any config model that can validate itself."""

    def validate_safe(self) -> list[str]:
        """Return warning strings. Empty list means fully valid."""
        ...
