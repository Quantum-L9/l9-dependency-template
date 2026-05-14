# Agent Brief — Play {{PLAY_NUMBER}}: {{REPO_NAME}}

## Mission
Create the `{{PACKAGE_NAME}}` dependency package inside the `cryptoxdog` org.
This package {{DESCRIPTION}}.

## Hard Rules
- Zero stubs. Every function must be implemented.
- All tests must pass before pushing.
- Never modify files outside `src/{{PACKAGE_NAME}}/` and `tests/` once injected.
- Never re-run a step whose `.done` checkpoint exists.

## DONEs — play is complete when ALL of these are true
- [ ] GitHub repo `cryptoxdog/{{REPO_NAME}}` exists
- [ ] Package renamed from `constellation_template` to `{{PACKAGE_NAME}}`
- [ ] `capability/` files injected into `src/{{PACKAGE_NAME}}/`
- [ ] `ruff check` passes with zero errors
- [ ] `mypy src` passes with zero errors
- [ ] `pytest tests/unit/ -q` passes (all green)
- [ ] PR merged to `main`
- [ ] Branch protection active on `main`
- [ ] `PLAY{{PLAY_NUMBER}}_COMPLETE.json` written to `$PLAY_DIR`

## Scripts Location (after cloning template)
```
$PLAY_DIR/_runner/tools/dep-build-runner/scripts/
```

## Execution Order
01_preflight → 02_create_repo → 03_bootstrap → 04_inject → 05_validate → 06_push → 07_verify
