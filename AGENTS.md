# AGENTS.md — constellation-template

Cross-tool agent instructions for this repository.
Read by Claude Code, Codex, Cursor, Copilot, Jules, Aider, CodeRabbit, and all AGENTS.md-compatible tools.

---

## 1. Mission of This Repo

`constellation-template` is the canonical scaffold for all `constellation_*` birth-dependency packages
in the L9 Constellation architecture.

This repo owns:
- The verified foundation layer every `constellation_*` package shares
- Canonical `pyproject.toml`, config, errors, AGENTS.md, CI, and Makefile patterns
- The rename workflow for bootstrapping new packages

This repo does **not** own:
- Any domain-specific logic (belongs in `domain-*` packages)
- Transport or routing (belongs in `constellation_node_sdk`)
- Gate registry or routing authority (belongs in `constellation_gate`)

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full layer model, dependency direction rules, and naming conventions.

---

## 2. Cardinal Laws (Non-Negotiable)

### 2.1 Infrastructure layer only

This package and all packages derived from it are `layer: [infrastructure]`.
Dependency direction is strictly upward: `domain-*` → `constellation_*` → `constellation_node_sdk`.
See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full layer model.

### 2.2 Safe-at-import contract

`get_<capability>_config()` MUST never raise on a clean node with no env vars set.
All config fields MUST have safe defaults.

### 2.3 Stable public API from v1.0.0

Symbols in `__all__` are stable. Additions are additive (minor bump).
Removals and renames are breaking (major bump). Never silently remove or rename exports.

---

## 3. Source-of-Truth Files

- `src/constellation_template/config.py` — config model and env var contract
- `src/constellation_template/errors.py` — exception hierarchy
- `src/constellation_template/__init__.py` — public API surface
- `pyproject.toml` — dependency and packaging contract

---

## 4. Change Policy

### 4.1 Allowed

- Bug fixes in any module
- Adding new config fields with safe defaults
- Adding new exception subclasses
- Test additions
- Docs improvements
- CI hardening

### 4.2 High-Risk (Requires Review)

- Renaming or removing fields from the config model (breaks existing nodes)
- Changing env var names (breaks existing deployments)
- Changing `__all__` to remove symbols (breaks consumers)
- Changing the `L9_<CAPABILITY>_` prefix convention

---

## 5. Code Standards

- Python 3.12+, `from __future__ import annotations` on every file
- Type hints on every function signature
- Pydantic v2 `BaseModel` for all structured data — `frozen=True, extra="forbid"` always
- `structlog.get_logger(__name__)` for logging — never configure structlog in library code
- All env vars use `L9_<CAPABILITY>_` prefix; never use bare names or collide with `L9_` transport vars
- `ruff format .` (100-char, Black-compatible) before commit
- `mypy --strict` must pass
- Exception messages: `msg = f"..."; raise ValueError(msg)` (avoids EM101)
- Nullable: `x: str | None = None` — never `Optional`
- Datetime: `datetime.now(tz=UTC)` always
- Unbounded caches: forbidden — use `cachetools.TTLCache` or equivalent
- Prefer `model_copy(update=...)` over in-place mutation
- Fail closed, not open

---

## 6. Testing Rules

Every new module needs at least one unit test.

### Required test scope by area

#### Config changes
Add/update `tests/unit/test_config.py` — safe defaults, env var loading, kill switch, cache clear.

#### Error hierarchy changes
Add/update `tests/unit/test_errors.py` — inheritance, raise, catch at base class.

#### Public API changes
Add/update `tests/unit/test_public_api.py` — all `__all__` symbols importable.

#### Integration changes
Add/update `tests/integration/` — real I/O, testcontainers, or tmp dirs as needed.

---

## 7. Validation Workflow Before Merge

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
- Register HTTP routes, mount sub-applications, or call `create_node_app()` from library code
- Add required config fields without safe defaults
- Remove `enabled` from any config model
- Remove `<Capability>Error` base class
- Rename or remove symbols from `__all__` without a major version bump
- Log PII values
- Create unbounded caches
- Use `eval()`, `exec()`, `pickle.load()`, or `yaml.load()` without SafeLoader
- Commit `.env` files, API keys, or secrets
- Hardcode tenant IDs, absolute paths, or environment-specific values

---

## 9. PR Checklist

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

## 10. Final Principle

This repo is the shared foundation that makes every `constellation_*` package consistent,
predictable, and safe to install on any node at birth.
