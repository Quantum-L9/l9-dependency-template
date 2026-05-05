# Changelog

All notable changes to `constellation-template` are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]

## [1.0.0] — 2026-05-04

### Added
- Initial canonical scaffold for all `constellation_*` birth-dependency packages.
- `TemplateConfig` — frozen Pydantic v2 config model with `L9_TEMPLATE_ENABLED` kill switch.
- `get_template_config()` — `@lru_cache` factory, safe-at-import, no required env vars.
- `TemplateError` hierarchy (`TemplateConfigError`, `TemplateRuntimeError`).
- `AGENTS.md` — 10-section canonical agent contract for infrastructure packages.
- `ARCHITECTURE.md` — layer model, dependency direction rule, birth stack, rename workflow, naming convention table.
- `Makefile` — `setup / dev / test / test-unit / test-integration / lint / lint-fix / clean`.
- `.pre-commit-config.yaml` — ruff + mypy hooks.
- `.github/workflows/ci.yml` — install → lint → import smoke → config smoke → kill-switch smoke → unit → integration.
- `tests/unit/test_public_api.py` — `__all__` import smoke + `__version__` check.
- `tests/unit/test_config.py` — safe defaults, kill switch, frozen model, extra-field rejection.
- `tests/unit/test_errors.py` — hierarchy, catch-at-base.
- `tests/unit/conftest.py` + `tests/integration/conftest.py` — `clear_config_cache` autouse fixture.
