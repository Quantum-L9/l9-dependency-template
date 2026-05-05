"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [errors, exceptions]
owner: platform-team
status: active
--- /L9_META ---

Exception hierarchy for constellation_template.

All public exceptions inherit from TemplateError so callers can catch the
package boundary with a single except clause.
Replace 'Template' throughout when bootstrapping a new package.
"""
from __future__ import annotations


class TemplateError(Exception):
    """Base exception for all constellation_template errors."""


class TemplateConfigError(TemplateError):
    """Raised when configuration is invalid or cannot be loaded."""


class TemplateRuntimeError(TemplateError):
    """Raised when a runtime operation fails."""
