# Agent Brief — Play 2: Constellation.PacketEnvelope

## Mission
Create the `constellation_packet_envelope` dependency package inside the `cryptoxdog` org.
This package defines the canonical PacketEnvelope schema and serialisation for all L9 inter-node transport.

## Context
- Template source: `cryptoxdog/Constellation.PackageTemplate`
- Runner scripts: cloned at `_runner/tools/dep-build-runner/scripts/`
- This is a **dependency package** — no FastAPI server.

## Hard Rules
- Zero stubs — every function implemented, typed, tested.
- Never modify files outside `src/constellation_packet_envelope/` and `tests/unit/`.
- Never re-run a step whose `.done` checkpoint exists.
- `ruff`, `mypy`, `pytest` must all be green before pushing.

## DONEs
- [ ] Repo `cryptoxdog/Constellation.PacketEnvelope` exists
- [ ] Package renamed `constellation_template` → `constellation_packet_envelope`
- [ ] `capability/` injected
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
