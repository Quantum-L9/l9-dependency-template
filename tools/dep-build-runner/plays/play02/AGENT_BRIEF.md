# Agent Brief — Play 2: Constellation.TransportPacket

## Mission
Create the `constellation_transport_packet` dependency package inside the `cryptoxdog` org.
This package implements the canonical `TransportPacket` Pydantic v2 frozen model with
immutable `derive()`, `with_hop()`, and `with_delegation()` builders for all L9 inter-node
transport.

> **INV-TP invariants are the contract this package must satisfy — no deviation.**  
> `PacketEnvelope` is fully deprecated (DEPR-001). This package MUST NOT reference it.

## Context
- Template source: `cryptoxdog/Constellation.PackageTemplate`
- Runner scripts: cloned at `_runner/tools/dep-build-runner/scripts/`
- This is a **dependency package** — no FastAPI server.

## Hard Rules
- Zero stubs — every function implemented, typed, tested.
- Never modify files outside `src/constellation_transport_packet/` and `tests/unit/`.
- Never re-run a step whose `.done` checkpoint exists.
- `ruff`, `mypy`, `pytest` must all be green before pushing.
- MUST NOT import, reference, or define `PacketEnvelope` anywhere (DEPR-001 = merge-block).

## Required capability/ files
- `models.py` — `TransportPacket` Pydantic v2 frozen model: `header`, `payload`, `governance`, `security`, `lineage`, `hop_trace`, `delegation_chain`
- `builders.py` — `derive()`, `with_hop()`, `with_delegation()` returning new instances (immutable; hop_trace append-only per INV-TP-04)
- `hashing.py` — `content_hash` SHA-256 over canonical payload bytes, excluding `hop_trace` per INV-TP-05
- `__init__.py` — re-exports `TransportPacket`, `derive`, `with_hop`, `with_delegation`
- `test_transport_packet.py` — tests: round-trip serde, derive preserves lineage, with_hop is append-only, hash stable across hops, no `PacketEnvelope` symbol present

## DONEs
- [ ] Repo `cryptoxdog/Constellation.TransportPacket` exists
- [ ] Package renamed `constellation_template` → `constellation_transport_packet`
- [ ] `capability/` injected
- [ ] Zero occurrences of `PacketEnvelope` in src or tests (grep must return empty)
- [ ] `ruff check` zero errors
- [ ] `mypy src` zero errors
- [ ] `pytest tests/unit/ -q` all green
- [ ] PR merged to `main`
- [ ] Branch protection active on `main`
- [ ] `PLAY2_COMPLETE.json` written to `$PLAY_DIR`

## Execution
```bash
export PLAY_DIR=/tmp/play02
mkdir -p $PLAY_DIR && cd $PLAY_DIR
# copy config.yaml, capability/, AGENT_BRIEF.md here
gh repo clone cryptoxdog/Constellation.PackageTemplate _runner
RUNNER=$PLAY_DIR/_runner/tools/dep-build-runner/scripts
bash $RUNNER/01_preflight.sh
bash $RUNNER/02_create_repo.sh
bash $RUNNER/03_bootstrap.sh
bash $RUNNER/04_inject.sh
bash $RUNNER/05_validate.sh
bash $RUNNER/06_push.sh
python3 $RUNNER/07_verify.py
```
