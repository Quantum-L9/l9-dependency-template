# Constellation.PackageTemplate

Canonical scaffold for all `constellation_*` birth-dependency packages in the L9 Constellation architecture.

## What this is

Every `constellation_*` infrastructure package shares an identical foundation layer.
This repo is that foundation. Clone → rename `<capability>` → write unique logic. Done.

The entire foundation (pyproject, config, errors, AGENTS.md, CI, Makefile, tests) is pre-built
and pre-validated. Build cycles for new packages start at the unique logic layer, not from scratch.

---

## Bootstrap a New Package

```bash
git clone https://github.com/cryptoxdog/Constellation.PackageTemplate Constellation.<Capability>
cd Constellation.<Capability>
git remote set-url origin https://github.com/cryptoxdog/Constellation.<Capability>

# Rename all placeholders (replace ingest/Ingest/INGEST with your capability)
find . -type f \( -name "*.py" -o -name "*.toml" -o -name "*.yaml" -o -name "*.md" \) \
  | xargs sed -i \
      -e 's/constellation_template/constellation_<capability>/g' \
      -e 's/constellation-template/constellation-<capability>/g' \
      -e 's/TemplateConfig/<Capability>Config/g' \
      -e 's/TemplateConfigError/<Capability>ConfigError/g' \
      -e 's/TemplateRuntimeError/<Capability>RuntimeError/g' \
      -e 's/TemplateError/<Capability>Error/g' \
      -e 's/get_template_config/get_<capability>_config/g' \
      -e 's/L9_TEMPLATE_/L9_<CAPABILITY>_/g'

mv src/constellation_template src/constellation_<capability>

# Verify
pip install -e ".[dev]"
make test

# Push
git add .
git commit -m "feat: bootstrap constellation_<capability> from Constellation.PackageTemplate"
git push -u origin main
```

---

## What to Add (Unique Logic Only)

After renaming, every new package only needs:

1. **Config fields** — add to `<Capability>Config` with safe defaults + `L9_<CAPABILITY>_*` env vars
2. **Logic modules** — add under `src/constellation_<capability>/`
3. **Public exports** — add to `__init__.py` `__all__`
4. **Unit tests** — add under `tests/unit/`
5. **CLI entrypoint** — uncomment `[project.scripts]` in `pyproject.toml` if needed
6. **Extras** — add `[project.optional-dependencies]` extras for optional heavy deps

---

## Birth Dependency Acceptance Gate

Every `constellation_*` package must pass all three before shipping to nodes:

```
1. pip install <package>           → succeeds in a clean venv
2. from <package> import X         → works with zero config
3. get_<capability>_config()       → returns safe defaults, never raises
```

---

## Layer Model

```
domain-*               →  imports constellation_* + constellation_node_sdk
constellation_*        →  imports constellation_node_sdk only  ← THIS LAYER
constellation_node_sdk →  imports nothing within constellation
```

---

## Naming Convention

| Dimension       | Pattern                      | Example                  |
|-----------------|------------------------------|--------------------------|
| PyPI name       | `constellation-<capability>` | `constellation-ingest`   |
| Python import   | `constellation_<capability>` | `constellation_ingest`   |
| Env prefix      | `L9_<CAPABILITY>_`           | `L9_INGEST_`             |
| GitHub repo     | `Constellation.<Capability>` | `Constellation.Ingest`   |
| Config class    | `<Capability>Config`         | `IngestConfig`           |
| Config factory  | `get_<capability>_config()`  | `get_ingest_config()`    |
| Base exception  | `<Capability>Error`          | `IngestError`            |

---

## Authority Order

`user_latest_instruction` > `active_artifact` > `source_files` > `kernel`

Unknowns are labeled `Unknown`. Nothing is fabricated.
