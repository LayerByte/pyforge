from __future__ import annotations

import os
import re
import secrets
import string
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pyforge.errors import ValidationError


def generate_uuids(count: int = 1) -> list[str]:
    if count < 1 or count > 1000:
        raise ValidationError("count must be between 1 and 1000")
    return [str(uuid.uuid4()) for _ in range(count)]


def convert_timestamp(value: str) -> dict[str, Any]:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"invalid ISO timestamp: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    utc = parsed.astimezone(timezone.utc)
    return {"utc": utc.isoformat(), "unix": utc.timestamp()}


def unix_time(value: float | None = None) -> dict[str, Any]:
    timestamp = time.time() if value is None else value
    try:
        moment = datetime.fromtimestamp(timestamp, timezone.utc)
    except (ValueError, OSError, OverflowError) as exc:
        raise ValidationError(f"invalid Unix timestamp: {timestamp}") from exc
    return {"unix": timestamp, "utc": moment.isoformat()}


def random_string(length: int = 32, include_symbols: bool = True) -> str:
    if length < 1 or length > 4096:
        raise ValidationError("length must be between 1 and 4096")
    alphabet = string.ascii_letters + string.digits + ("!@#$%^&*()-_=+" if include_symbols else "")
    return "".join(secrets.choice(alphabet) for _ in range(length))


def developer_json_format(value: str, indent: int = 2) -> str:
    from pyforge.tools.json_tools.core import format_json

    return format_json(value, indent=indent)


def developer_regex_test(pattern: str, text: str) -> list[dict[str, object]]:
    from pyforge.tools.text.core import regex_test

    return regex_test(pattern, text)


def convert_color(value: str) -> dict[str, Any]:
    text = value.strip()
    if re.fullmatch(r"#?[0-9a-fA-F]{6}", text):
        raw = text.lstrip("#")
        rgb = tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))
        return {"hex": "#" + raw.upper(), "rgb": rgb}
    match = re.fullmatch(r"\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*", text)
    if match:
        rgb = tuple(map(int, match.groups()))
        if all(0 <= item <= 255 for item in rgb):
            return {"hex": "#" + "".join(f"{item:02X}" for item in rgb), "rgb": rgb}
    raise ValidationError("color must be RRGGBB or r,g,b")


def developer_url_parser(value: str) -> dict[str, Any]:
    from pyforge.tools.network.core import parse_url

    return parse_url(value)


def explain_cron(expression: str) -> str:
    presets = {
        "* * * * *": "Every minute",
        "0 * * * *": "At minute 0 of every hour",
        "0 0 * * *": "Every day at midnight",
        "0 0 * * 0": "Every Sunday at midnight",
        "0 0 1 * *": "On day 1 of every month at midnight",
    }
    value = " ".join(expression.split())
    if value in presets:
        return presets[value]
    fields = value.split()
    if len(fields) != 5:
        raise ValidationError("cron expression must contain five fields")
    labels = ("minute", "hour", "day of month", "month", "day of week")
    return "; ".join(f"{label}: {field}" for label, field in zip(labels, fields, strict=True))


def environment_variables(prefix: str = "") -> dict[str, str]:
    sensitive = ("KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL")
    return {
        key: ("[REDACTED]" if any(word in key.upper() for word in sensitive) else value)
        for key, value in sorted(os.environ.items())
        if key.startswith(prefix)
    }


def project_structure(directory: str | Path, max_depth: int = 3) -> list[str]:
    from pyforge.tools.files.core import directory_tree

    return directory_tree(directory, max_depth=max_depth)


def source_line_count(directory: str | Path) -> dict[str, Any]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    comment = {
        ".py": "#",
        ".rb": "#",
        ".sh": "#",
        ".c": "//",
        ".cpp": "//",
        ".h": "//",
        ".hpp": "//",
        ".kt": "//",
        ".rs": "//",
        ".swift": "//",
    }
    totals = {"files": 0, "code": 0, "comments": 0, "blank": 0}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in comment:
            totals["files"] += 1
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    totals["blank"] += 1
                elif stripped.startswith(comment[path.suffix.lower()]):
                    totals["comments"] += 1
                else:
                    totals["code"] += 1
    return totals
