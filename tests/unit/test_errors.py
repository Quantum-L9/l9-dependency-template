"""Unit tests for the exception hierarchy and ErrorCode enum."""

from __future__ import annotations

from constellation_template.errors import (
    ErrorCode,
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
            msg = "test"
            raise exc_class(msg)
        except TemplateError:
            pass
        else:
            msg = f"{exc_class} not caught by TemplateError"
            raise AssertionError(msg)


def test_default_code_is_unknown() -> None:
    assert TemplateError("oops").code == ErrorCode.UNKNOWN.value


def test_config_error_default_code() -> None:
    assert TemplateConfigError("bad").code == ErrorCode.CONFIG_INVALID.value


def test_runtime_error_default_code() -> None:
    assert TemplateRuntimeError("boom").code == ErrorCode.RUNTIME_FAILURE.value


def test_custom_code_enum() -> None:
    assert (
        TemplateError("t", code=ErrorCode.RUNTIME_TIMEOUT).code == ErrorCode.RUNTIME_TIMEOUT.value
    )


def test_custom_code_string() -> None:
    assert TemplateError("t", code="MY_CODE").code == "MY_CODE"


def test_context_stored() -> None:
    ctx = {"env": "prod"}
    assert TemplateError("t", context=ctx).context == ctx


def test_context_defaults_empty() -> None:
    assert TemplateError("t").context == {}


def test_cause_stored_and_chained() -> None:
    original = ValueError("root")
    exc = TemplateRuntimeError("wrapped", cause=original)
    assert exc.cause is original
    assert exc.__cause__ is original


def test_repr_contains_code() -> None:
    assert "TEMPLATE_CONFIG_MISSING" in repr(TemplateError("t", code=ErrorCode.CONFIG_MISSING))


def test_error_code_enum_values_are_strings() -> None:
    for member in ErrorCode:
        assert isinstance(member.value, str)


def test_error_code_str_subclass() -> None:
    assert issubclass(ErrorCode, str)
