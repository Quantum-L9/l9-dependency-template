#!/usr/bin/env python3
"""Sets branch protection on main requiring the CI validate check."""
import os, subprocess, json, sys
from pathlib import Path
import yaml

PLAY_DIR = Path(os.environ.get("PLAY_DIR", Path.cwd()))
cfg = yaml.safe_load((PLAY_DIR / "config.yaml").read_text())
repo = f"{cfg['org']}/{cfg['repo_name']}"

payload = {
    "required_status_checks": {
        "strict": True,
        "contexts": ["validate"],
    },
    "enforce_admins": False,
    "required_pull_request_reviews": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews": True,
    },
    "restrictions": None,
}

r = subprocess.run(
    ["gh", "api", f"repos/{repo}/branches/main/protection",
     "--method", "PUT", "--input", "-"],
    input=json.dumps(payload).encode(),
    capture_output=True,
)
if r.returncode != 0:
    print(f"branch protection warning: {r.stderr.decode()}", file=sys.stderr)
    sys.exit(1)
print(f"Branch protection set on {repo}/main")
