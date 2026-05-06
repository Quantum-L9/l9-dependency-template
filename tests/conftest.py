"""Root conftest — shared session-scoped fixtures for all test scopes."""
from __future__ import annotations

import pytest


@pytest.fixture(scope="session", autouse=True)
def _verify_package_importable() -> None:
    """Fail fast if the package cannot be imported at all."""
    import constellation_template  # noqa: F401
