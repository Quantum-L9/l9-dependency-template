"""Unit tests for the exception hierarchy."""
from __future__ import annotations

from constellation_template.errors import (
    TemplateConfigError,
    TemplateError,
    TemplateRuntimeError,
)


def test_template_error_is_exception() -> None:
    assert issubclass(TemplateError, Exception)


def test_config_error_inherits_base() -> None:
    assert issubclass(TemplateConfigError, TemplateError)


def test_runtime_error_inherits_base() -> None:
    assert issubclass(TemplateRuntimeError, TemplateError)


def test_catch_at_base() -> None:
    for exc_class in (TemplateConfigError, TemplateRuntimeError):
        try:
            raise exc_class("test")
        except TemplateError:
            pass
        else:
            raise AssertionError(f"{exc_class} not caught by TemplateError")
