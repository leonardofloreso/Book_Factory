from __future__ import annotations

def chapter_to_markdown(chapter: dict) -> str:
    lines: list[str] = []
    lines.append(f"# {chapter['title']}")
    lines.append("")
    for section in chapter["sections"]:
        lines.append(f"## {section['heading']}")
        lines.append("")
        for p in section["paragraphs"]:
            lines.append(p.strip())
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
