#!/usr/bin/env bash
set -euo pipefail
PLAY_DIR="${PLAY_DIR:-$(pwd)}"
CHECKPOINT="$PLAY_DIR/.checkpoints/03_bootstrap.done"
[[ -f "$CHECKPOINT" ]] && echo "03 already done." && exit 0

echo "=== 03_bootstrap ==="
eval "$(python3 - <<'PYEOF'
import yaml, os
cfg = yaml.safe_load(open(os.environ["PLAY_DIR"] + "/config.yaml"))
print(f"ORG={cfg['org']}")
print(f"REPO_NAME={cfg['repo_name']}")
print(f"PACKAGE_NAME={cfg['package_name']}")
print(f"REPO_SLUG={cfg['package_name'].replace('_','-')}")
print(f"WORK_DIR={cfg['work_dir']}")
PYEOF
)"

TEMPLATE_REPO="cryptoxdog/Constellation.PackageTemplate"
OLD_PKG="constellation_template"
OLD_SLUG="constellation-template"
DEST="${WORK_DIR}/${REPO_NAME}"

mkdir -p "$WORK_DIR"

if [[ -d "$DEST/.git" ]]; then
    echo "Scaffold already exists at $DEST, skipping clone."
else
    gh repo clone "${TEMPLATE_REPO}" "${DEST}"
    cd "${DEST}"

    # Strip template history, wire to new remote
    rm -rf .git
    git init -b main
    git remote add origin "https://github.com/${ORG}/${REPO_NAME}.git"

    # Rename package directory
    if [[ -d "src/${OLD_PKG}" ]]; then
        mv "src/${OLD_PKG}" "src/${PACKAGE_NAME}"
    fi

    # Patch all constellation_template references
    find . -type f \( -name "*.toml" -o -name "*.yml" -o -name "*.yaml" -o -name "*.py" -o -name "*.md" \) \
        ! -path "./.git/*" \
        -exec sed -i "s/${OLD_PKG}/${PACKAGE_NAME}/g" {} +

    find . -type f \( -name "*.toml" -o -name "*.yml" \) \
        ! -path "./.git/*" \
        -exec sed -i "s/${OLD_SLUG}/${REPO_SLUG}/g" {} +

    uv sync --extra dev
fi

touch "$PLAY_DIR/.checkpoints/03_bootstrap.done"
echo "03_bootstrap PASSED — scaffold at ${DEST}"
