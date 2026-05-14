#!/usr/bin/env bash
set -euo pipefail
PLAY_DIR="${PLAY_DIR:-$(pwd)}"
CHECKPOINT="$PLAY_DIR/.checkpoints/01_preflight.done"
[[ -f "$CHECKPOINT" ]] && echo "01 already done." && exit 0

echo "=== 01_preflight ==="
fail() { echo "FAIL: $1" >&2; exit 1; }

command -v git     >/dev/null 2>&1 || fail "git not found"
command -v gh      >/dev/null 2>&1 || fail "gh CLI not found"
command -v python3 >/dev/null 2>&1 || fail "python3 not found"
command -v uv      >/dev/null 2>&1 || fail "uv not found"

python3 -c "import yaml" 2>/dev/null || pip install pyyaml -q

gh auth status >/dev/null 2>&1 || fail "gh not authenticated — run: gh auth login"

CONFIG="$PLAY_DIR/config.yaml"
[[ -f "$CONFIG" ]] || fail "config.yaml not found in $PLAY_DIR"

python3 - <<'PYEOF'
import yaml, sys, os
cfg = yaml.safe_load(open(os.environ["PLAY_DIR"] + "/config.yaml"))
required = ["org","repo_name","package_name","description","play_number","work_dir"]
missing = [k for k in required if not cfg.get(k)]
if missing:
    print(f"config.yaml missing keys: {missing}", file=sys.stderr); sys.exit(1)
if "CHANGE_ME" in cfg["repo_name"]:
    print("config.yaml still has CHANGE_ME placeholder", file=sys.stderr); sys.exit(1)
print("config.yaml OK")
PYEOF

[[ -d "$PLAY_DIR/capability" ]] || fail "capability/ directory not found in $PLAY_DIR"

mkdir -p "$PLAY_DIR/.checkpoints"
touch "$CHECKPOINT"
echo "01_preflight PASSED"
