from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from pyforge.errors import ToolExecutionError, ValidationError


def _git(repository: str | Path, *arguments: str) -> str:
    root = Path(repository)
    if not root.exists():
        raise ValidationError(f"repository does not exist: {root}")
    process = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if process.returncode != 0:
        raise ToolExecutionError(process.stderr.strip() or "git command failed")
    return process.stdout.strip()


def repository_information(repository: str | Path = ".") -> dict[str, Any]:
    root = _git(repository, "rev-parse", "--show-toplevel")
    branch = _git(repository, "branch", "--show-current")
    remotes = _git(repository, "remote", "-v").splitlines()
    changed = _git(repository, "status", "--porcelain").splitlines()
    return {"root": root, "branch": branch or "[detached]", "remotes": remotes, "clean": not changed}


def current_branch(repository: str | Path = ".") -> str:
    return _git(repository, "branch", "--show-current") or "[detached HEAD]"


def branch_list(repository: str | Path = ".") -> list[dict[str, Any]]:
    output = _git(repository, "branch", "--format=%(HEAD)%09%(refname:short)")
    return [
        {"name": line.split("	", 1)[1], "current": line.startswith("*")}
        for line in output.splitlines()
        if "	" in line
    ]


def commit_history(repository: str | Path = ".", limit: int = 20) -> list[dict[str, str]]:
    if limit < 1 or limit > 500:
        raise ValidationError("limit must be between 1 and 500")
    output = _git(repository, "log", f"-{limit}", "--date=iso-strict", "--pretty=format:%h%x09%ad%x09%an%x09%s")
    result = []
    for line in output.splitlines():
        parts = line.split("	", 3)
        if len(parts) == 4:
            result.append(dict(zip(("hash", "date", "author", "subject"), parts, strict=True)))
    return result


def contributor_summary(repository: str | Path = ".") -> list[dict[str, Any]]:
    counts = Counter(_git(repository, "log", "--format=%aN <%aE>").splitlines())
    return [{"contributor": name, "commits": count} for name, count in counts.most_common()]


def repository_statistics(repository: str | Path = ".") -> dict[str, Any]:
    files = _git(repository, "ls-files").splitlines()
    commits = int(_git(repository, "rev-list", "--count", "HEAD") or 0)
    extensions = Counter(Path(path).suffix.lower() or "[none]" for path in files)
    return {"tracked_files": len(files), "commits": commits, "extensions": dict(extensions.most_common())}


def changed_files(repository: str | Path = ".") -> list[dict[str, str]]:
    result = []
    for line in _git(repository, "status", "--porcelain=v1", "--untracked-files=no").splitlines():
        if len(line) >= 4:
            result.append({"index": line[0], "worktree": line[1], "path": line[3:]})
    return result


def untracked_files(repository: str | Path = ".") -> list[str]:
    return _git(repository, "ls-files", "--others", "--exclude-standard").splitlines()


def gitignore_check(repository: str | Path, paths: list[str]) -> list[dict[str, Any]]:
    if not paths:
        raise ValidationError("at least one path is required")
    result = []
    for path in paths:
        process = subprocess.run(
            ["git", "-C", str(repository), "check-ignore", "-v", path],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        result.append({"path": path, "ignored": process.returncode == 0, "rule": process.stdout.strip() or None})
    return result


def large_tracked_files(repository: str | Path = ".", minimum_bytes: int = 10_000_000) -> list[dict[str, Any]]:
    if minimum_bytes < 0:
        raise ValidationError("minimum_bytes cannot be negative")
    root = Path(_git(repository, "rev-parse", "--show-toplevel"))
    result = []
    for relative in _git(repository, "ls-files").splitlines():
        path = root / relative
        try:
            size = path.stat().st_size
            if size >= minimum_bytes:
                result.append({"path": relative, "size": size})
        except OSError:
            continue
    return sorted(result, key=lambda row: row["size"], reverse=True)
