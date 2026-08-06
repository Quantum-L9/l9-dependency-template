# Constellation.PackageTemplate

Canonical scaffold for all `constellation_*` birth-dependency packages in the L9 Constellation architecture.

Every `constellation_*` infrastructure package shares an identical foundation layer.
Clone → rename `<capability>` → write unique logic. Done.

The entire foundation (`pyproject.toml`, config, errors, health, AGENTS.md, CI, Makefile, tests) is
pre-built and pre-validated. Build cycles for new packages start at the unique logic layer, not from scratch.

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the layer model, dependency direction rules, and naming conventions.

---

## Bootstrap a New Package

```bash
git clone https://github.com/cryptoxdog/Constellation.PackageTemplate Constellation.<Capability>
cd Constellation.<Capability>
git remote set-url origin https://github.com/cryptoxdog/Constellation.<Capability>

# Rename all placeholders.
# IMPORTANT: subclasses (ConfigError, RuntimeError) MUST come before the base (Error).
find . -type f \( -name "*.py" -o -name "*.toml" -o -name "*.yaml" -o -name "*.md" \) \
  | xargs sed -i \
      -e 's/constellation_template/constellation_<capability>/g' \
      -e 's/constellation-template/constellation-<capability>/g' \
      -e 's/TemplateConfigError/<Capability>ConfigError/g' \
      -e 's/TemplateRuntimeError/<Capability>RuntimeError/g' \
      -e 's/TemplateError/<Capability>Error/g' \
      -e 's/TemplateConfig/<Capability>Config/g' \
      -e 's/get_template_config/get_<capability>_config/g' \
      -e 's/L9_TEMPLATE_/L9_<CAPABILITY>_/g'

mv src/constellation_template src/constellation_<capability>

pip install -e ".[dev]"
make test

git add .
git commit -m "feat: bootstrap constellation_<capability> from Constellation.PackageTemplate"
git push -u origin main
```

---

## What to Add (Unique Logic Only)

After renaming, a new package only needs:

1. **Config fields** — add to `<Capability>Config` with safe defaults; `L9_<CAPABILITY>_*` env vars are read automatically via `env_prefix`
2. **Logic modules** — add under `src/constellation_<capability>/`
3. **Public exports** — add to `__init__.py` `__all__`
4. **Unit tests** — add under `tests/unit/`
5. **Health details** — extend `health.py` `details` dict with capability-specific readiness info
6. **CLI entrypoint** — uncomment `[project.scripts]` in `pyproject.toml` if needed
7. **Extras** — add `[project.optional-dependencies]` extras for optional heavy deps

---

## Birth Dependency Acceptance Gate

Every `constellation_*` package must pass all three before shipping to nodes:

```
1. pip install <package>           → succeeds in a clean venv
2. from <package> import X         → works with zero config
3. get_<capability>_config()       → returns safe defaults, never raises
```
