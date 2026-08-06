#!/usr/bin/env python3
"""Final verification gate — writes PLAY{N}_COMPLETE.json on success."""
import json, os, subprocess, sys
from pathlib import Path
import yaml

PLAY_DIR = Path(os.environ.get("PLAY_DIR", Path.cwd()))
cfg = yaml.safe_load((PLAY_DIR / "config.yaml").read_text())

ORG      = cfg["org"]
REPO     = cfg["repo_name"]
PLAY_NUM = cfg["play_number"]
PKG      = cfg["package_name"]
WORK_DIR = Path(cfg["work_dir"])
DEST     = WORK_DIR / REPO

errors: list[str] = []

def check(label: str, cond: bool) -> None:
    mark = "OK  " if cond else "FAIL"
    print(f"  [{mark}] {label}")
    if not cond:
        errors.append(label)

for step in ["01_preflight","02_create_repo","03_bootstrap",
             "04_inject","05_validate","06_push"]:
    check(f"checkpoint {step}",
          (PLAY_DIR / ".checkpoints" / f"{step}.done").exists())

r = subprocess.run(["gh","repo","view",f"{ORG}/{REPO}"], capture_output=True)
check(f"repo {ORG}/{REPO} exists", r.returncode == 0)

check(f"src/{PKG}/ exists", (DEST / "src" / PKG).is_dir())

r = subprocess.run(
    ["gh","pr","list","--repo",f"{ORG}/{REPO}","--state","open","--json","number"],
    capture_output=True, text=True)
open_prs = json.loads(r.stdout or "[]")
check("no open PRs remaining", len(open_prs) == 0)

if errors:
    print(f"\nVERIFICATION FAILED: {errors}", file=sys.stderr)
    sys.exit(1)

out = PLAY_DIR / f"PLAY{PLAY_NUM}_COMPLETE.json"
out.write_text(json.dumps(
    {"play": PLAY_NUM, "repo": f"{ORG}/{REPO}",
     "package": PKG, "status": "complete"}, indent=2))
print(f"\nPLAY {PLAY_NUM} COMPLETE — {out}")
