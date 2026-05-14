# L9 Dependency Build Runner

Reusable automation that builds **L9 Constellation dependency packages** from a
`Constellation.PackageTemplate` scaffold.  
Lives inside the template itself — the tool is built into the thing it builds.

## Terminology

| Term | Meaning |
|------|---------|
| **Dependency package** | A `constellation_*` Python package (typed, tested, PyPI-publishable) |
| **Play** | One numbered execution that creates exactly one dependency package |
| **Play pack** | The 3-item payload an AI agent receives to run a play |

Plays 1–8 each create one dependency package that the L9 Constellation nodes consume.

## Play Pack (what an agent receives per play)

```
play-config.yaml          ← 6 fields: org, repo_name, package_name, description, play_number, work_dir
AGENT_BRIEF.md            ← mission + DONEs filled in for this play
capability/               ← 5 domain files: config.py, models.py, core.py, __init__.py, test_unit.py
```

## How an Agent Runs a Play

```bash
# 1. Set working directory for this play
export PLAY_DIR=/tmp/play${N}
mkdir -p $PLAY_DIR
cd $PLAY_DIR

# 2. Copy play pack files here
cp play-config.yaml config.yaml
cp AGENT_BRIEF.md .
cp -r capability/ .

# 3. Clone template to get the runner scripts
gh repo clone cryptoxdog/Constellation.PackageTemplate _runner
RUNNER=$PLAY_DIR/_runner/tools/dep-build-runner/scripts

# 4. Execute steps in order (each is idempotent via .checkpoints/)
bash $RUNNER/01_preflight.sh
bash $RUNNER/02_create_repo.sh
bash $RUNNER/03_bootstrap.sh
bash $RUNNER/04_inject.sh
bash $RUNNER/05_validate.sh
bash $RUNNER/06_push.sh
python3 $RUNNER/07_verify.py
```

## Checkpoint Recovery

Each script writes `$PLAY_DIR/.checkpoints/NN_name.done` on success.  
If a step fails, fix the issue and re-run the same script — it skips already-done steps.

## config.yaml Fields

```yaml
org: "cryptoxdog"
repo_name: "Constellation.MyPackage"     # exact GitHub repo name
package_name: "constellation_my_package" # Python-importable name (underscores)
description: "One-line description"
play_number: 1
work_dir: "/tmp/l9-plays"
```

## Plays Index

| Play | Repo | Package |
|------|------|---------|
| 1 | Constellation.ReadmeValidator | constellation_readme_validator |
| 2 | Constellation.PacketEnvelope | constellation_packet_envelope |
| 3 | Constellation.SchemaRegistry | constellation_schema_registry |
| 4 | Constellation.LineageGraph | constellation_lineage_graph |
| 5 | Constellation.PolicyEngine | constellation_policy_engine |
| 6 | Constellation.AuditLogger | constellation_audit_logger |
| 7 | Constellation.HealthProbe | constellation_health_probe |
| 8 | Constellation.ConfigLoader | constellation_config_loader |
