from __future__ import annotations
from pathlib import Path

def build_manifest(run_dir: Path) -> dict:
    # Minimal manifest: list files
    files = []
    for p in sorted(run_dir.rglob("*")):
        if p.is_file():
            files.append(str(p.relative_to(run_dir)))
    return {"run_dir": str(run_dir), "files": files}
