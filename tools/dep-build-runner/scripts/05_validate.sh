#!/usr/bin/env bash
set -euo pipefail
PLAY_DIR="${PLAY_DIR:-$(pwd)}"
CHECKPOINT="$PLAY_DIR/.checkpoints/05_validate.done"
[[ -f "$CHECKPOINT" ]] && echo "05 already done." && exit 0

echo "=== 05_validate ==="
eval "$(python3 - <<'PYEOF'
import yaml, os
cfg = yaml.safe_load(open(os.environ["PLAY_DIR"] + "/config.yaml"))
print(f"REPO_NAME={cfg['repo_name']}")
print(f"WORK_DIR={cfg['work_dir']}")
PYEOF
)"

DEST="${WORK_DIR}/${REPO_NAME}"
cd "${DEST}"

echo "--- ruff ---"
uv run ruff check src tests

echo "--- mypy ---"
uv run mypy src

echo "--- pytest ---"
uv run pytest tests/unit/ -q --tb=short

touch "$PLAY_DIR/.checkpoints/05_validate.done"
echo "05_validate PASSED"
