from __future__ import annotations
import os
from .llm_stub import plan_outline_stub, write_chapter_stub

def _mode() -> str:
    return os.getenv("LLM_MODE", "stub").strip().lower()

def plan_outline(book_input: dict) -> dict:
    # Future: if _mode() == "gemini": ...
    return plan_outline_stub(book_input)

def write_chapter(book_input: dict, chapter_spec: dict, used_phrases: dict | None = None) -> dict:
    return write_chapter_stub(book_input, chapter_spec, used_phrases=used_phrases)

