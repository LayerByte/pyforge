from __future__ import annotations

from pathlib import Path
from typing import Any

from pyforge.errors import ValidationError


def export_txt(data: Any, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, dict):
        text = "\n".join(f"{key}: {value}" for key, value in data.items())
    elif isinstance(data, list):
        text = "\n".join(str(item) for item in data)
    else:
        text = str(data)
    target.write_text(text + "\n", encoding="utf-8")
    return target


def export_json(data: Any, path: str | Path) -> Path:
    import json

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    return target


def export_csv(data: Any, path: str | Path) -> Path:
    import csv

    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
        rows = data
    else:
        raise ValidationError("CSV export requires a mapping or list of mappings")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return target
