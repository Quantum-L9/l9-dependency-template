# Architecture — Constellation Package Template

## Layer Model

```
Layer 3 — Routing Engine
  constellation_gate
  Not installed by nodes. Runs as the routing process.

Layer 2 — Domain Services
  domain-*
  Business logic. Depends on Layer 0 + Layer 1. Never imported by infrastructure.

Layer 1 — Universal Infrastructure  ← THIS LAYER
  constellation_* packages (this template)
  File I/O, caching, chunking, observability, storage, auth helpers.
  Zero domain logic. Zero HTTP routes. Safe to install on any node.

Layer 0 — Transport Contract
  constellation_node_sdk
  GateClient, create_node_app, TransportPacket, signing, handlers.
  Every node installs this at birth. Never grows domain logic.
```

## Dependency Direction Rule

```
constellation_gate        (no upstream deps within constellation)
domain-*               →  may import constellation_node_sdk + constellation_* infra
constellation_*        →  may import constellation_node_sdk ONLY
constellation_node_sdk →  imports nothing within constellation
```

Arrows go one direction only: upward.
If a Layer 1 package imports from a `domain-*` package, the abstraction is in the wrong layer.

## Birth Stack

Every new node installs these at creation time, in order:

```
1. constellation_node_sdk     — always, no exceptions
2. constellation_ingest       — if node reads files or repos
3. constellation_obs          — (future) structured telemetry
4. constellation_store        — (future) storage adapters
5. constellation_auth         — (future) extended auth helpers
6. domain-<name>              — the node's unique business logic
```

## Birth Dependency Acceptance Gate

Every `constellation_*` package must answer YES to all three before shipping:

```
1. pip install <package>             → succeeds in a clean venv
2. from <package> import X           → works with zero config
3. get_<capability>_config()         → returns safe defaults, no crash
```

## Rename Workflow (Bootstrap a New Package)

```bash
git clone https://github.com/cryptoxdog/Constellation.PackageTemplate Constellation.<Capability>
cd Constellation.<Capability>
git remote set-url origin https://github.com/cryptoxdog/Constellation.<Capability>

# Rename placeholders — IMPORTANT: subclasses MUST be renamed before the base class.
# Replace <capability>, <Capability>, <CAPABILITY> with your actual values before running.
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

# Verify rename
pip install -e ".[dev]"
make test

# Push
git add .
git commit -m "feat: bootstrap constellation_<capability> from Constellation.PackageTemplate"
git push -u origin main
```

## Package Naming Convention

| Dimension | Pattern | Example |
|---|---|---|
| PyPI name | `constellation-<capability>` | `constellation-ingest` |
| Python import | `constellation_<capability>` | `constellation_ingest` |
| Env var prefix | `L9_<CAPABILITY>_` | `L9_INGEST_` |
| GitHub repo | `Constellation.<Capability>` | `Constellation.Ingest` |
| Config class | `<Capability>Config` | `IngestConfig` |
| Config factory | `get_<capability>_config()` | `get_ingest_config()` |
| Base exception | `<Capability>Error` | `IngestError` |
