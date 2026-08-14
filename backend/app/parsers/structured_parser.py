import json
from pathlib import Path

from app.schemas.parsed import ParsedStructured


def parse_json(filepath: Path) -> ParsedStructured:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"'{filepath.name}' is not valid JSON: {e}")

    top_level_keys: list[str] = []
    item_count: int | None = None

    if isinstance(data, dict):
        top_level_keys = list(data.keys())
    elif isinstance(data, list):
        item_count = len(data)

    return ParsedStructured(
        filename=filepath.name,
        file_type="json",
        data=data,
        top_level_keys=top_level_keys,
        item_count=item_count,
    )