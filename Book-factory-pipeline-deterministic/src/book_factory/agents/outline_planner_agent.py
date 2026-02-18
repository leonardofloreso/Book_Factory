from __future__ import annotations
from .llm_router import plan_outline

class OutlinePlannerAgent:
    def run(self, book_input: dict) -> dict:
        return plan_outline(book_input)
