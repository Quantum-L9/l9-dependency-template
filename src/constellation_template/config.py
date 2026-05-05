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
All env vars use the L9_TEMPLATE_ prefix to avoid collision with the L9_
transport vars owned by constellation_node_sdk.
"""
from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel, ConfigDict


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class TemplateConfig(BaseModel):
    """Runtime configuration for constellation_template.

    Loaded once per process via get_template_config().
    All fields have safe defaults — import never raises.
    Frozen and strict: no extra fields, no mutation.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = True
    """Master kill switch. Set L9_TEMPLATE_ENABLED=false to disable all behaviour."""

    # ---------------------------------------------------------------------------
    # Add capability-specific fields below.
    # Each field MUST have a safe default so get_template_config() never raises.
    # Read from L9_TEMPLATE_<FIELD> env vars in get_template_config().
    # ---------------------------------------------------------------------------


@lru_cache
def get_template_config() -> TemplateConfig:
    """Return the process-level TemplateConfig singleton.

    Reads from L9_TEMPLATE_* environment variables.
    Safe to call at import time on any node with no env vars configured.
    Call get_template_config.cache_clear() in tests to reset between cases.
    """
    return TemplateConfig(
        enabled=_env_bool("L9_TEMPLATE_ENABLED", True),
        # Map additional fields here from L9_TEMPLATE_* env vars.
    )
