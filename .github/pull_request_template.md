## Summary
<!-- What does this PR do? One sentence. -->

## Type
- [ ] Bug fix
- [ ] New feature / capability field
- [ ] Hardening / CI improvement
- [ ] Docs / AGENTS.md update
- [ ] Template scaffold update

## PR Checklist
- [ ] No `domain-*` imports introduced
- [ ] No HTTP route registration introduced
- [ ] `get_<capability>_config()` still safe to call with no env vars set
- [ ] All new env vars use `L9_<CAPABILITY>_` prefix with safe defaults
- [ ] `__all__` updated if new public symbols added
- [ ] `py.typed` present
- [ ] `L9_META` block present on new non-trivial modules
- [ ] `ruff check src tests` exits 0
- [ ] `mypy src` exits 0
- [ ] `pytest -q` exits 0
- [ ] `make security` exits 0
- [ ] No secrets, `.env` files, or hardcoded values committed
- [ ] `CHANGELOG.md` updated
