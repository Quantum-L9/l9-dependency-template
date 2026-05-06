"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [config, env, pydantic]
owner: platform-team
status: active
--- /L9_META ---

Configuration model for constellation_template.

Replace 'Template' / 'TEMPLATE' throughout when bootstrapping a new package.
All env vars use the L9_TEMPLATE_ prefix (via env_prefix in SettingsConfigDict)
to avoid collision with L9_ transport vars owned by constellation_node_sdk.
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

    # ---------------------------------------------------------------------------
    # Add capability-specific fields below.
    # Each field MUST have a safe default so get_template_config() never raises.
    # pydantic-settings reads them from L9_TEMPLATE_<FIELDNAME> automatically.
    # ---------------------------------------------------------------------------

    def validate_safe(self) -> list[str]:
        """Return a list of warning strings. Empty list means fully valid.

        Never raises. Called by health_check() and any CLI --check command.
        Add capability-specific validation checks in derived packages.
        """
        warnings: list[str] = []
        if not self.enabled:
            warnings.append("capability is disabled via L9_TEMPLATE_ENABLED=false")
        return warnings


@lru_cache
def get_template_config() -> TemplateConfig:
    """Return the process-level TemplateConfig singleton.

    Reads from L9_TEMPLATE_* environment variables via pydantic-settings.
    Safe to call at import time on any node with no env vars configured.
    Call get_template_config.cache_clear() in tests to reset between cases.
    """
    return TemplateConfig()
