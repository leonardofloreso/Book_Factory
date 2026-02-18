from __future__ import annotations
from pathlib import Path

def assemble_book(chapters_dir: Path) -> str:
    # Concatenate chapter .md files in order ch1.md, ch2.md...
    md_files = sorted(chapters_dir.glob("ch*.md"), key=lambda p: int(p.stem.replace("ch", "")))
    parts = []
    for p in md_files:
        parts.append(p.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts).strip() + "\n"
