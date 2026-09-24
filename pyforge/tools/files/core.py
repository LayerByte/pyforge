from __future__ import annotations

import filecmp
import fnmatch
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pyforge.errors import ValidationError


def file_information(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    try:
        metadata = target.stat()
    except OSError as exc:
        raise ValidationError(f"cannot inspect {target}: {exc}") from exc
    return {
        "path": str(target.resolve()),
        "name": target.name,
        "suffix": target.suffix,
        "size": metadata.st_size,
        "is_file": target.is_file(),
        "is_directory": target.is_dir(),
        "modified": datetime.fromtimestamp(metadata.st_mtime, timezone.utc).isoformat(),
        "permissions": oct(metadata.st_mode & 0o777),
    }


def file_hash(path: str | Path, algorithm: str = "sha256") -> str:
    name = algorithm.lower().replace("-", "")
    if name not in {"md5", "sha1", "sha256", "sha384", "sha512"}:
        raise ValidationError(f"unsupported hash algorithm: {algorithm}")
    digest = hashlib.new(name)
    try:
        with Path(path).open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise ValidationError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def compare_files(first: str | Path, second: str | Path) -> dict[str, Any]:
    left, right = Path(first), Path(second)
    if not left.is_file() or not right.is_file():
        raise ValidationError("both comparison paths must be readable files")
    return {
        "same_size": left.stat().st_size == right.stat().st_size,
        "same_content": filecmp.cmp(left, right, shallow=False),
        "first": str(left),
        "second": str(right),
    }


def find_duplicates(directory: str | Path) -> list[list[str]]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    sizes: dict[int, list[Path]] = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file():
            try:
                sizes[path.stat().st_size].append(path)
            except OSError:
                continue
    groups: dict[str, list[str]] = defaultdict(list)
    for paths in sizes.values():
        if len(paths) > 1:
            for path in paths:
                groups[file_hash(path)].append(str(path))
    return [items for items in groups.values() if len(items) > 1]


def directory_statistics(directory: str | Path) -> dict[str, Any]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    files = directories = bytes_total = 0
    extensions: Counter[str] = Counter()
    for path in root.rglob("*"):
        if path.is_dir():
            directories += 1
        elif path.is_file():
            files += 1
            extensions[path.suffix.lower() or "[none]"] += 1
            try:
                bytes_total += path.stat().st_size
            except OSError:
                pass
    return {
        "files": files,
        "directories": directories,
        "bytes": bytes_total,
        "extensions": dict(extensions.most_common()),
    }


def directory_tree(directory: str | Path, max_depth: int = 4) -> list[str]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    if max_depth < 0:
        raise ValidationError("max_depth must be non-negative")
    lines = [f"{root.name}/"]

    def visit(current: Path, prefix: str, depth: int) -> None:
        if depth >= max_depth:
            return
        try:
            entries = sorted(current.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except OSError:
            return
        for index, path in enumerate(entries):
            last = index == len(entries) - 1
            lines.append(f"{prefix}{'`-- ' if last else '|-- '}{path.name}{'/' if path.is_dir() else ''}")
            if path.is_dir():
                visit(path, prefix + ("    " if last else "|   "), depth + 1)

    visit(root, "", 0)
    return lines


def search_files(directory: str | Path, pattern: str) -> list[str]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    if not pattern:
        raise ValidationError("pattern cannot be empty")
    return sorted(str(path) for path in root.rglob("*") if path.is_file() and fnmatch.fnmatch(path.name, pattern))


def find_large_files(directory: str | Path, minimum_bytes: int = 100_000_000) -> list[dict[str, Any]]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    if minimum_bytes < 0:
        raise ValidationError("minimum_bytes cannot be negative")
    found = []
    for path in root.rglob("*"):
        try:
            if path.is_file() and path.stat().st_size >= minimum_bytes:
                found.append({"path": str(path), "size": path.stat().st_size})
        except OSError:
            continue
    return sorted(found, key=lambda item: item["size"], reverse=True)


def find_empty_files(directory: str | Path) -> list[str]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    result = []
    for path in root.rglob("*"):
        try:
            if path.is_file() and path.stat().st_size == 0:
                result.append(str(path))
        except OSError:
            continue
    return sorted(result)


def extension_statistics(directory: str | Path) -> dict[str, int]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    counts = Counter(path.suffix.lower() or "[none]" for path in root.rglob("*") if path.is_file())
    return dict(counts.most_common())


def integrity_snapshot(directory: str | Path) -> dict[str, str]:
    root = Path(directory)
    if not root.is_dir():
        raise ValidationError(f"not a directory: {root}")
    snapshot = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            snapshot[path.relative_to(root).as_posix()] = file_hash(path, "sha256")
    return snapshot
