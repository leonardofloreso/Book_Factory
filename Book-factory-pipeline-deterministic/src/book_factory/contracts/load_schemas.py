from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def load_all_schemas(schemas_dir: Path) -> Dict[str, Dict[str, Any]]:
    return {
        "input_book": load_json(schemas_dir / "input_book.schema.json"),
        "outline": load_json(schemas_dir / "outline.schema.json"),
        "chapter": load_json(schemas_dir / "chapter.schema.json"),
    }
