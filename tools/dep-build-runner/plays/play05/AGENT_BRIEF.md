# Agent Brief — Play 5: Constellation.PolicyEngine

## Mission
Create the `constellation_policy_engine` dependency package inside the `cryptoxdog` org.
This package evaluates OPA-backed policies against PacketEnvelope payloads.

## Context
- Template source: `cryptoxdog/Constellation.PackageTemplate`
- Runner scripts: cloned at `_runner/tools/dep-build-runner/scripts/`
- This is a **dependency package** — no FastAPI server.

## Hard Rules
- Zero stubs — every function implemented, typed, tested.
- Never modify files outside `src/constellation_policy_engine/` and `tests/unit/`.
- Never re-run a step whose `.done` checkpoint exists.

## DONEs
- [ ] Repo `cryptoxdog/Constellation.PolicyEngine` exists
- [ ] Package renamed `constellation_template` → `constellation_policy_engine`
- [ ] `capability/` injected
- [ ] `ruff check` zero errors
- [ ] `mypy src` zero errors
- [ ] `pytest tests/unit/ -q` all green
- [ ] PR merged to `main`
- [ ] Branch protection active on `main`
- [ ] `PLAY5_COMPLETE.json` written to `$PLAY_DIR`

## Execution
```bash
export PLAY_DIR=/tmp/play05
mkdir -p $PLAY_DIR && cd $PLAY_DIR
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
