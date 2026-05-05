from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def clear_config_cache() -> None:  # type: ignore[return]
    """Clear lru_cache on get_template_config before and after each integration test."""
    from constellation_template.config import get_template_config

    get_template_config.cache_clear()
    yield
    get_template_config.cache_clear()
