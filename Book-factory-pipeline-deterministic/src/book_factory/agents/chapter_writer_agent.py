from __future__ import annotations
from .llm_router import write_chapter

class ChapterWriterAgent:
    def run(self, book_input: dict, chapter_spec: dict, used_phrases: dict | None = None) -> dict:
        return write_chapter(book_input, chapter_spec, used_phrases=used_phrases)

