from __future__ import annotations

import hashlib
import hmac
from pathlib import Path

from pyforge.errors import ValidationError

ALGORITHMS = {"md5", "sha1", "sha256", "sha384", "sha512"}


def _algorithm(name: str) -> str:
    normalized = name.lower().replace("-", "")
    if normalized not in ALGORITHMS:
        raise ValidationError(f"unsupported hash algorithm: {name}")
    return normalized


def hash_text(text: str, algorithm: str = "sha256") -> str:
    return hashlib.new(_algorithm(algorithm), text.encode("utf-8")).hexdigest()


def hash_file(path: str | Path, algorithm: str = "sha256") -> str:
    digest = hashlib.new(_algorithm(algorithm))
    try:
        with Path(path).open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise ValidationError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def compare_hashes(expected: str, actual: str) -> bool:
    left = "".join(expected.split()).lower()
    right = "".join(actual.split()).lower()
    if not left or not right:
        raise ValidationError("hash values cannot be empty")
    return hmac.compare_digest(left, right)
