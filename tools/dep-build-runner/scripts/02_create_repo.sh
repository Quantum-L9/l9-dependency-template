#!/usr/bin/env bash
set -euo pipefail
PLAY_DIR="${PLAY_DIR:-$(pwd)}"
CHECKPOINT="$PLAY_DIR/.checkpoints/02_create_repo.done"
[[ -f "$CHECKPOINT" ]] && echo "02 already done." && exit 0

echo "=== 02_create_repo ==="
eval "$(python3 - <<'PYEOF'
import yaml, os
cfg = yaml.safe_load(open(os.environ["PLAY_DIR"] + "/config.yaml"))
print(f"ORG={cfg['org']}")
print(f"REPO_NAME={cfg['repo_name']}")
print(f"DESCRIPTION={cfg['description']}")
PYEOF
)"

if gh repo view "${ORG}/${REPO_NAME}" >/dev/null 2>&1; then
    echo "Repo ${ORG}/${REPO_NAME} already exists, skipping create."
else
    gh repo create "${ORG}/${REPO_NAME}" \
        --private \
        --description "${DESCRIPTION}"
    echo "Created ${ORG}/${REPO_NAME}"
fi

touch "$PLAY_DIR/.checkpoints/02_create_repo.done"
echo "02_create_repo PASSED"
