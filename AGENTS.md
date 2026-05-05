# AGENTS.md — constellation-template

Cross-tool agent instructions for this repository.
Read by Claude Code, Codex, Cursor, Copilot, Jules, Aider, CodeRabbit, and all AGENTS.md-compatible tools.

---

## 1. Mission of this repo

`constellation-template` is the canonical scaffold for all `constellation_*` birth-dependency packages in the L9 Constellation architecture.

This repo owns:
- The verified foundation layer every `constellation_*` package shares
- Canonical `pyproject.toml`, config, errors, AGENTS.md, CI, and Makefile patterns
- The rename workflow for bootstrapping new packages

This repo does **not** own:
- Any domain-specific logic (that belongs in `domain-*` packages)
- Transport or routing (that belongs in `constellation_node_sdk`)
- Gate registry or routing authority (that belongs in `constellation_gate`)

---

## 2. Non-negotiable architectural laws

### 2.1 Infrastructure layer only
This package and all packages derived from it are `layer: [infrastructure]`.
They MUST NOT import from `domain-*` packages.
Dependency direction: `domain-*` → `constellation_*` → `constellation_node_sdk`. Never reversed.

### 2.2 Safe-at-import contract
`get_<capability>_config()` MUST never raise on a clean node with no env vars set.
All fields MUST have safe defaults.

### 2.3 No HTTP route registration
Infrastructure packages MUST NOT register FastAPI routes, mount sub-applications,
or call `create_node_app()`. HTTP is owned by the chassis layer.

### 2.4 L9_<CAPABILITY>_ env prefix exclusively
All env vars use `L9_<CAPABILITY>_` prefix. Never use bare names.
Never collide with `L9_` transport vars owned by `constellation_node_sdk`.

### 2.5 Stable public API from v1.0.0
Symbols in `__all__` are stable. Additions are additive (minor bump).
Removals are breaking (major bump). Never silently remove exports.

---

## 3. Source-of-truth files

- `src/constellation_template/config.py` — config model and env var contract
- `src/constellation_template/errors.py` — exception hierarchy
- `src/constellation_template/__init__.py` — public API surface
- `pyproject.toml` — dependency and packaging contract

---

## 4. Change policy

### 4.1 Allowed changes
- Bug fixes in any module
- Adding new config fields with safe defaults
- Adding new exception subclasses
- Test additions
- Docs improvements
- CI hardening

### 4.2 High-risk changes
- Renaming or removing fields from the config model (breaks existing nodes)
- Changing env var names (breaks existing deployments)
- Changing `__all__` to remove symbols (breaks consumers)
- Changing the `L9_<CAPABILITY>_` prefix convention

### 4.3 Forbidden changes
- Importing from `domain-*` packages
- Registering HTTP routes from library code
- Adding required config fields with no safe default
- Removing `enabled` from config
- Removing `TemplateError` base class
- Hardcoding env-specific values, tenant IDs, secrets, or absolute paths

---

## 5. Code standards

- Python 3.12+, `from __future__ import annotations` on every file
- Type hints on every function signature
- Pydantic v2 `BaseModel` for all structured data — `frozen=True, extra="forbid"` always
- `structlog.get_logger(__name__)` for logging — never configure structlog in library code
- `ruff format .` (100-char, Black-compatible) before commit
- `mypy --strict` must pass
- Exception messages: `msg = f"..."; raise ValueError(msg)` (avoids EM101)
- Nullable: `x: str | None = None` — never `Optional`
- Datetime: `datetime.now(tz=UTC)` always
- Unbounded caches: forbidden — use `cachetools.TTLCache` or equivalent
- `eval()`, `exec()`, `pickle.load()`, `yaml.load()` without SafeLoader: forbidden
- Prefer `model_copy(update=...)` over in-place mutation
- Fail closed, not open

---

## 6. Testing rules

Every new module needs at least one unit test.

### Required test scope by area

#### Config changes
Add/update:
- `tests/unit/test_config.py` — safe defaults, env var loading, kill switch, cache clear

#### Error hierarchy changes
Add/update:
- `tests/unit/test_errors.py` — inheritance, raise, catch at base class

#### Public API changes
Add/update:
- `tests/unit/test_public_api.py` — all `__all__` symbols importable

#### Integration changes
Add/update:
- `tests/integration/` — real I/O, testcontainers, or tmp dirs as needed

---

## 7. Validation workflow before merge

```bash
pip install -e ".[dev]"
ruff check src tests
mypy src
pytest -q
```

All four commands must exit 0 before merge.

---

## 8. Boundaries

### ✅ Always
- Use `frozen=True, extra="forbid"` on every config model
- Use `@lru_cache` on every config factory
- Use `L9_<CAPABILITY>_` prefix for every env var
- Include `enabled: bool = True` as the first config field
- Include `py.typed` in the package root
- Emit `L9_META` block at the top of every non-trivial module

### ⚠️ Ask First
- Adding a new optional dependency (may affect install surface of all consumers)
- Changing the `[project.scripts]` CLI entrypoint name (breaks existing callers)
- Adding a new `[project.optional-dependencies]` extra
- Adding a new env var (must follow `L9_<CAPABILITY>_` prefix and have a safe default)

### 🚫 Never
- Import from `domain-*` packages
- Register HTTP routes from library code
- Add required config fields without safe defaults
- Log PII values
- Create unbounded caches
- Commit `.env` files, API keys, or secrets
- Hardcode tenant IDs, absolute paths, or environment-specific values

---

## 9. PR checklist

- [ ] No `domain-*` imports introduced
- [ ] No HTTP route registration introduced
- [ ] `get_<capability>_config()` still safe to call with no env vars set
- [ ] All new env vars use `L9_<CAPABILITY>_` prefix with safe defaults
- [ ] `__all__` updated if new public symbols added
- [ ] `py.typed` present
- [ ] `L9_META` block present on new modules
- [ ] `ruff check src tests` exits 0
- [ ] `mypy src` exits 0
- [ ] `pytest -q` exits 0
- [ ] No secrets, `.env` files, or hardcoded values committed

---

## 10. Final principle

This repo is the shared foundation that makes every `constellation_*` package consistent, predictable, and safe to install on any node at birth.
