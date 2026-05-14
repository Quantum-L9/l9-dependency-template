#!/usr/bin/env python3
"""Writes README.meta.yaml into cwd (should be DEST repo root)."""
import os
from pathlib import Path
import yaml

PLAY_DIR = Path(os.environ.get("PLAY_DIR", Path.cwd()))
cfg = yaml.safe_load((PLAY_DIR / "config.yaml").read_text())

meta = {
    "schema_version": "1.0",
    "package": {
        "name": cfg["package_name"],
        "repo": f"{cfg['org']}/{cfg['repo_name']}",
        "description": cfg["description"],
        "play_number": cfg["play_number"],
    },
    "ownership": {"org": cfg["org"], "team": "l9-constellation"},
    "scope": {
        "owns": [f"src/{cfg['package_name']}"],
        "forbidden": ["tools/", "pyproject.toml (schema)"],
    },
}

out = Path.cwd() / "README.meta.yaml"
out.write_text(yaml.dump(meta, sort_keys=False))
print(f"Wrote {out}")
