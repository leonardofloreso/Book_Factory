from __future__ import annotations

def guard_text(text: str, forbidden_tokens: list[str]) -> None:
    for tok in forbidden_tokens:
        if tok and tok in text:
            raise ValueError(f"Forbidden token detected: {tok!r}")

def guard_paragraphs(paragraphs: list[str], forbidden_tokens: list[str]) -> None:
    for p in paragraphs:
        guard_text(p, forbidden_tokens)
        if len(p.strip()) < 20:
            raise ValueError("Paragraph too short (min 20 chars).")
