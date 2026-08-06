"""
--- L9_META ---
l9_schema: 1
origin: constellation-template
layer: [infrastructure]
tags: [errors, exceptions]
owner: platform-team
status: active
--- /L9_META ---
"""

from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    UNKNOWN = "TEMPLATE_UNKNOWN"
    CONFIG_INVALID = "TEMPLATE_CONFIG_INVALID"
    CONFIG_MISSING = "TEMPLATE_CONFIG_MISSING"
    RUNTIME_FAILURE = "TEMPLATE_RUNTIME_FAILURE"
    RUNTIME_TIMEOUT = "TEMPLATE_RUNTIME_TIMEOUT"


class TemplateError(Exception):
    """Base exception for all constellation_template errors.

    Structured fields allow direct structlog logging without string formatting:
        log.error("operation failed", code=exc.code, **exc.context)
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | ErrorCode = ErrorCode.UNKNOWN,
        context: dict[str, object] | None = None,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.code: str = code.value if isinstance(code, ErrorCode) else code
        self.context: dict[str, object] = context or {}
        self.cause: BaseException | None = cause
        if cause is not None:
            self.__cause__ = cause

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.args[0]!r}, code={self.code!r}, context={self.context!r})"
        )


class TemplateConfigError(TemplateError):
    """Raised when configuration is invalid or cannot be loaded."""

    def __init__(
        self,
        message: str,
        *,
        code: str | ErrorCode = ErrorCode.CONFIG_INVALID,
        context: dict[str, object] | None = None,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message, code=code, context=context, cause=cause)


class TemplateRuntimeError(TemplateError):
    """Raised when a runtime operation fails."""

    def __init__(
        self,
        message: str,
        *,
        code: str | ErrorCode = ErrorCode.RUNTIME_FAILURE,
        context: dict[str, object] | None = None,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message, code=code, context=context, cause=cause)
