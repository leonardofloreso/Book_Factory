from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    repo_root: Path
    schemas_dir: Path
    outputs_dir: Path

def get_settings() -> Settings:
    repo_root = Path(__file__).resolve().parents[2]  # .../src/book_factory/config.py -> repo root
    return Settings(
        repo_root=repo_root,
        schemas_dir=repo_root / "schemas",
        outputs_dir=repo_root / "outputs",
    )
