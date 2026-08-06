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

## Dependency Direction

```
constellation_gate        (no upstream deps within constellation)
domain-*               →  may import constellation_node_sdk + constellation_* infra
constellation_*        →  may import constellation_node_sdk ONLY
constellation_node_sdk →  imports nothing within constellation
```

Arrows flow upward only. A Layer 1 package that imports from a `domain-*` package is in the wrong layer.

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

## Package Naming Convention

| Dimension       | Pattern                      | Example                  |
|-----------------|------------------------------|--------------------------|
| PyPI name       | `constellation-<capability>` | `constellation-ingest`   |
| Python import   | `constellation_<capability>` | `constellation_ingest`   |
| Env prefix      | `L9_<CAPABILITY>_`           | `L9_INGEST_`             |
| GitHub repo     | `Constellation.<Capability>` | `Constellation.Ingest`   |
| Config class    | `<Capability>Config`         | `IngestConfig`           |
| Config factory  | `get_<capability>_config()`  | `get_ingest_config()`    |
| Base exception  | `<Capability>Error`          | `IngestError`            |
