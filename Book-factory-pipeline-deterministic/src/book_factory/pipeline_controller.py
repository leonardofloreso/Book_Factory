from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import get_settings
from .contracts.load_schemas import load_all_schemas
from .contracts.paths import build_run_paths
from .validation.schema_validator import SchemaValidator
from .validation.format_guard import guard_paragraphs
from .rendering.markdown_renderer import chapter_to_markdown
from .artifacts.io import ensure_dir, read_json, write_json, write_text
from .artifacts.book_assembler import assemble_book
from .artifacts.manifest_builder import build_manifest
from .agents.outline_planner_agent import OutlinePlannerAgent
from .agents.chapter_writer_agent import ChapterWriterAgent


@dataclass
class PipelineController:
    def __post_init__(self) -> None:
        s = get_settings()
        self.settings = s
        self.schemas = load_all_schemas(s.schemas_dir)
        self.validators = {
            "input_book": SchemaValidator(self.schemas["input_book"]),
            "outline": SchemaValidator(self.schemas["outline"]),
            "chapter": SchemaValidator(self.schemas["chapter"]),
        }
        self.outline_engine = OutlinePlannerAgent()
        self.chapter_engine = ChapterWriterAgent()

    def _new_run_dir(self, book_id: str) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.settings.outputs_dir / f"{book_id}_{ts}"

    # -------------------------
    # Public MVP entrypoint
    # -------------------------
    def run_all(self, input_path: Path) -> Path:
        """
        MVP: single command entrypoint.

        Reads input_book.json, generates outline, writes chapters (json+md),
        assembles full book, and produces manifest + run_report.
        """
        book_input = read_json(input_path)
        self.validators["input_book"].validate(book_input)

        run_dir = self._new_run_dir(book_input["book_id"])
        rp = build_run_paths(run_dir)

        # Ensure output structure
        ensure_dir(run_dir)
        ensure_dir(rp.chapters_dir)
        ensure_dir(rp.qa_dir)

        # Copy input into run folder (reproducibility)
        write_json(rp.input_copy_path, book_input)

        # Stage 1: plan outline (internal)
        outline = self.plan(book_input)
        write_json(rp.outline_path, outline)

        # Stage 2: write chapters (internal)
        self.write(book_input, outline, rp.chapters_dir)

        # Stage 3: artifacts
        self.finalize(run_dir, rp)

        return run_dir

    # -------------------------
    # Internal pipeline stages
    # -------------------------
    def plan(self, book_input: dict) -> dict:
        outline = self.outline_engine.run(book_input)
        self.validators["outline"].validate(outline)
        return outline

    def write(self, book_input: dict, outline: dict, chapters_dir: Path) -> None:
        forbidden = book_input["constraints"]["forbidden_tokens"]

        # NOTE: Keep used_phrases outside the loop if you want cross-chapter de-duplication.
        # For MVP, per-chapter uniqueness is acceptable and simpler.
        for chapter_spec in outline["chapters"]:
            used_phrases = {"openers": set(), "closers": set()}

            raw = self.chapter_engine.run(
                book_input,
                chapter_spec,
                used_phrases=used_phrases,
            )
            self.validators["chapter"].validate(raw)

            # Format guard
            for sec in raw["sections"]:
                guard_paragraphs(sec["paragraphs"], forbidden)

            # Persist JSON + MD
            ch_id = chapter_spec["chapter_id"]
            write_json(chapters_dir / f"{ch_id}.json", raw)
            write_text(chapters_dir / f"{ch_id}.md", chapter_to_markdown(raw))

    def finalize(self, run_dir: Path, rp) -> None:
        # Assemble full book
        full = assemble_book(rp.chapters_dir)
        write_text(rp.book_full_md_path, full)

        # Manifest + report
        write_json(rp.manifest_path, build_manifest(run_dir))
        write_json(
            rp.run_report_path,
            {
                "status": "ok",
                "command": "all",
                "run_dir": str(run_dir),
            },
        )
