"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [config, env, pydantic]
owner: platform-team
status: active
--- /L9_META ---
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class TemplateConfig(BaseSettings):
    """Runtime configuration for constellation_template.

    Loaded once per process via get_template_config().
    All fields have safe defaults — import never raises.
    Frozen and strict: no extra fields, no mutation.
    pydantic-settings reads L9_TEMPLATE_<FIELD> env vars automatically.
    """

    model_config = SettingsConfigDict(
        env_prefix="L9_TEMPLATE_",
        frozen=True,
        extra="forbid",
        populate_by_name=True,
    )

    enabled: bool = True
    """Master kill switch. Set L9_TEMPLATE_ENABLED=false to disable all behaviour."""

    def validate_safe(self) -> list[str]:
        """Return warning strings. Empty list means fully valid. Never raises."""
        warnings: list[str] = []
        if not self.enabled:
            warnings.append("capability is disabled via L9_TEMPLATE_ENABLED=false")
        return warnings


@lru_cache
def get_template_config() -> TemplateConfig:
    """Return the process-level TemplateConfig singleton.

    Thread-safe: lru_cache provides atomic construction in CPython 3.12+.
    Reads from L9_TEMPLATE_* environment variables via pydantic-settings.
    Safe to call at import time on any node with no env vars configured.
    Call get_template_config.cache_clear() in tests to reset between cases.
    """
    return TemplateConfig()
