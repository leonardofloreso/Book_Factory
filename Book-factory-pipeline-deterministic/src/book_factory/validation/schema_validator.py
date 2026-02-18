from __future__ import annotations
from typing import Any, Dict
from jsonschema import Draft7Validator

class SchemaValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.validator = Draft7Validator(schema)

    def validate(self, obj: Any) -> None:
        errors = sorted(self.validator.iter_errors(obj), key=lambda e: e.path)
        if errors:
            msg = "; ".join([f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors[:5]])
            raise ValueError(f"Schema validation failed: {msg}")
