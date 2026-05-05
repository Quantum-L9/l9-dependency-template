"""Smoke tests — every symbol in __all__ must be importable."""
from __future__ import annotations

import importlib

import constellation_template


def test_all_symbols_importable() -> None:
    for name in constellation_template.__all__:
        assert hasattr(constellation_template, name), f"missing from package: {name}"


def test_version_present() -> None:
    assert hasattr(constellation_template, "__version__")
    assert isinstance(constellation_template.__version__, str)
    assert constellation_template.__version__
