"""Unit tests for Configurable and HealthCheckable protocols."""

from __future__ import annotations

from constellation_template.health import health_check
from constellation_template.protocols import Configurable, HealthCheckable


class _MockHC:
    def check_health(self):
        return health_check()


class _MockConf:
    def validate_safe(self) -> list[str]:
        return []


def test_health_checkable_protocol_satisfied() -> None:
    assert isinstance(_MockHC(), HealthCheckable)


def test_configurable_protocol_satisfied() -> None:
    assert isinstance(_MockConf(), Configurable)


def test_protocol_is_runtime_checkable() -> None:
    assert isinstance(_MockHC(), HealthCheckable)
    assert isinstance(_MockConf(), Configurable)
