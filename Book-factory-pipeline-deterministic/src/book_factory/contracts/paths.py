from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class RunPaths:
    run_dir: Path
    input_copy_path: Path
    outline_path: Path
    chapters_dir: Path
    qa_dir: Path
    manifest_path: Path
    run_report_path: Path
    book_full_md_path: Path

def build_run_paths(run_dir: Path) -> RunPaths:
    chapters_dir = run_dir / "chapters"
    qa_dir = run_dir / "qa"
    return RunPaths(
        run_dir=run_dir,
        input_copy_path=run_dir / "input_book.json",
        outline_path=run_dir / "outline.json",
        chapters_dir=chapters_dir,
        qa_dir=qa_dir,
        manifest_path=run_dir / "manifest.json",
        run_report_path=run_dir / "run_report.json",
        book_full_md_path=run_dir / "book_full.md",
    )
