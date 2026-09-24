from __future__ import annotations

import json
from collections import Counter
from typing import Any

from pyforge.errors import ValidationError


def _load(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def format_json(value: str, indent: int = 2, sort_keys: bool = True) -> str:
    if indent not in range(1, 9):
        raise ValidationError("indent must be between 1 and 8")
    return json.dumps(_load(value), ensure_ascii=False, indent=indent, sort_keys=sort_keys)


def minify_json(value: str) -> str:
    return json.dumps(_load(value), ensure_ascii=False, separators=(",", ":"))


def validate_json(value: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
        return {"valid": True, "type": type(parsed).__name__, "error": None}
    except json.JSONDecodeError as exc:
        return {"valid": False, "type": None, "error": {"message": exc.msg, "line": exc.lineno, "column": exc.colno}}


def json_view(value: str) -> list[dict[str, Any]]:
    rows = []

    def visit(item: Any, path: str) -> None:
        if isinstance(item, dict):
            if not item:
                rows.append({"path": path or "$", "value": {}})
            for key, child in item.items():
                visit(child, f"{path}.{key}" if path else str(key))
        elif isinstance(item, list):
            if not item:
                rows.append({"path": path or "$", "value": []})
            for index, child in enumerate(item):
                visit(child, f"{path}[{index}]")
        else:
            rows.append({"path": path or "$", "value": item})

    visit(_load(value), "")
    return rows


def json_statistics(value: str) -> dict[str, Any]:
    counts = Counter()
    maximum = 0

    def visit(item: Any, depth: int) -> None:
        nonlocal maximum
        maximum = max(maximum, depth)
        if isinstance(item, dict):
            counts["objects"] += 1
            counts["keys"] += len(item)
            for child in item.values():
                visit(child, depth + 1)
        elif isinstance(item, list):
            counts["arrays"] += 1
            for child in item:
                visit(child, depth + 1)
        else:
            counts[type(item).__name__] += 1
            counts["values"] += 1

    visit(_load(value), 0)
    return {**counts, "max_depth": maximum}


def search_json_keys(value: str, query: str, case_sensitive: bool = False) -> list[dict[str, Any]]:
    if not query:
        raise ValidationError("query cannot be empty")
    needle = query if case_sensitive else query.casefold()
    found = []

    def visit(item: Any, path: str) -> None:
        if isinstance(item, dict):
            for key, child in item.items():
                current = f"{path}.{key}" if path else key
                candidate = key if case_sensitive else key.casefold()
                if needle in candidate:
                    found.append({"path": current, "value": child})
                visit(child, current)
        elif isinstance(item, list):
            for index, child in enumerate(item):
                visit(child, f"{path}[{index}]")

    visit(_load(value), "")
    return found


def compare_json(first: str, second: str) -> dict[str, Any]:
    left, right = _load(first), _load(second)
    differences = []

    def visit(a: Any, b: Any, path: str) -> None:
        if type(a) is not type(b):
            differences.append({"path": path or "$", "first": a, "second": b})
            return
        if isinstance(a, dict):
            for key in sorted(set(a) | set(b)):
                current = f"{path}.{key}" if path else key
                if key not in a or key not in b:
                    differences.append(
                        {"path": current, "first": a.get(key, "[missing]"), "second": b.get(key, "[missing]")}
                    )
                else:
                    visit(a[key], b[key], current)
        elif isinstance(a, list):
            for index in range(max(len(a), len(b))):
                current = f"{path}[{index}]"
                visit(a[index] if index < len(a) else "[missing]", b[index] if index < len(b) else "[missing]", current)
        elif a != b:
            differences.append({"path": path or "$", "first": a, "second": b})

    visit(left, right, "")
    return {"equal": not differences, "differences": differences}
