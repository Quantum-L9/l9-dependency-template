#!/usr/bin/env bash
set -euo pipefail
PLAY_DIR="${PLAY_DIR:-$(pwd)}"
CHECKPOINT="$PLAY_DIR/.checkpoints/04_inject.done"
[[ -f "$CHECKPOINT" ]] && echo "04 already done." && exit 0

echo "=== 04_inject ==="
eval "$(python3 - <<'PYEOF'
import yaml, os
cfg = yaml.safe_load(open(os.environ["PLAY_DIR"] + "/config.yaml"))
print(f"PACKAGE_NAME={cfg['package_name']}")
print(f"REPO_NAME={cfg['repo_name']}")
print(f"WORK_DIR={cfg['work_dir']}")
PYEOF
)"

DEST="${WORK_DIR}/${REPO_NAME}"
SRC_DIR="${DEST}/src/${PACKAGE_NAME}"
TESTS_DIR="${DEST}/tests/unit"

[[ -d "$PLAY_DIR/capability" ]] || { echo "FAIL: capability/ not found"; exit 1; }

for f in "$PLAY_DIR"/capability/*.py; do
    fname="$(basename "$f")"
    if [[ "$fname" == test_* ]]; then
        mkdir -p "$TESTS_DIR"
        cp "$f" "$TESTS_DIR/$fname"
        echo "  injected test: tests/unit/$fname"
    else
        mkdir -p "$SRC_DIR"
        cp "$f" "$SRC_DIR/$fname"
        echo "  injected src: src/${PACKAGE_NAME}/$fname"
    fi
done

cd "${DEST}"
python3 "$PLAY_DIR/_runner/tools/dep-build-runner/scripts/write_meta_yaml.py"

touch "$PLAY_DIR/.checkpoints/04_inject.done"
echo "04_inject PASSED"
