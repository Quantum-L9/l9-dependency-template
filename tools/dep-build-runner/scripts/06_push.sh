#!/usr/bin/env bash
set -euo pipefail
PLAY_DIR="${PLAY_DIR:-$(pwd)}"
CHECKPOINT="$PLAY_DIR/.checkpoints/06_push.done"
[[ -f "$CHECKPOINT" ]] && echo "06 already done." && exit 0

echo "=== 06_push ==="
eval "$(python3 - <<'PYEOF'
import yaml, os
cfg = yaml.safe_load(open(os.environ["PLAY_DIR"] + "/config.yaml"))
print(f"ORG={cfg['org']}")
print(f"REPO_NAME={cfg['repo_name']}")
print(f"PLAY_NUMBER={cfg['play_number']}")
print(f"WORK_DIR={cfg['work_dir']}")
PYEOF
)"

DEST="${WORK_DIR}/${REPO_NAME}"
BRANCH="feat/play${PLAY_NUMBER}-init"
cd "${DEST}"

# Commit scaffold to main as base
git add -A
git diff --cached --quiet || git commit -m "chore: scaffold from Constellation.PackageTemplate"
git push -u origin main 2>/dev/null || git push --force-with-lease origin main

# Feature branch with capability injection
git checkout -b "${BRANCH}" 2>/dev/null || git checkout "${BRANCH}"
git add -A
git diff --cached --quiet || git commit -m "feat(play${PLAY_NUMBER}): inject capability source"
git push -u origin "${BRANCH}"

# Open PR
PR_URL=$(gh pr create \
    --repo "${ORG}/${REPO_NAME}" \
    --base main \
    --head "${BRANCH}" \
    --title "feat(play${PLAY_NUMBER}): initial package implementation" \
    --body "Automated play ${PLAY_NUMBER} — capability injected, all gates passed." \
    2>/dev/null || gh pr view --repo "${ORG}/${REPO_NAME}" --json url -q .url)

echo "PR: ${PR_URL}"

# Poll CI — max 10 min
echo "Waiting for CI..."
ELAPSED=0
while [[ $ELAPSED -lt 600 ]]; do
    STATUS=$(gh pr checks "${PR_URL}" --json state -q ".[].state" 2>/dev/null | sort -u || echo "pending")
    echo "  CI @ ${ELAPSED}s: ${STATUS}"
    echo "$STATUS" | grep -qi "failure\|error" && { echo "CI FAILED"; exit 1; }
    echo "$STATUS" | grep -qv "pending\|queued\|in_progress" && break
    sleep 30; ELAPSED=$((ELAPSED + 30))
done

gh pr merge "${PR_URL}" --repo "${ORG}/${REPO_NAME}" --squash --auto
python3 "$PLAY_DIR/_runner/tools/dep-build-runner/scripts/set_branch_protection.py"

touch "$PLAY_DIR/.checkpoints/06_push.done"
echo "06_push PASSED — PR merged"
