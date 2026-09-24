from __future__ import annotations

import math
import os
import re
import socket
import ssl
import stat
from collections import Counter
from pathlib import Path
from typing import Any

from pyforge.errors import ToolExecutionError, ValidationError


def password_strength(password: str) -> dict[str, Any]:
    if not password:
        return {"score": 0, "rating": "empty", "feedback": ["Enter a password to analyze"]}
    score = min(len(password) * 4, 40)
    feedback = []
    checks = (
        (any(c.islower() for c in password), "lowercase"),
        (any(c.isupper() for c in password), "uppercase"),
        (any(c.isdigit() for c in password), "digits"),
        (any(not c.isalnum() for c in password), "symbols"),
    )
    score += sum(ok for ok, _ in checks) * 12
    for ok, label in checks:
        if not ok:
            feedback.append(f"Add {label}")
    if len(password) < 16:
        feedback.append("Use at least 16 characters")
    else:
        score += 12
    if re.search(r"(.)\1{2,}", password):
        score -= 15
        feedback.append("Avoid repeated characters")
    if any(word in password.casefold() for word in ("password", "qwerty", "letmein")):
        score -= 30
        feedback.append("Avoid common password patterns")
    score = max(0, min(score, 100))
    rating = "strong" if score >= 80 else "moderate" if score >= 55 else "weak"
    return {"score": score, "rating": rating, "feedback": feedback}


def check_file_hash(path: str | Path, expected: str, algorithm: str = "sha256") -> dict[str, Any]:
    from pyforge.tools.hashing.core import compare_hashes, hash_file

    actual = hash_file(path, algorithm)
    return {"match": compare_hashes(expected, actual), "algorithm": algorithm, "actual": actual}


def file_entropy(path: str | Path) -> dict[str, Any]:
    try:
        data = Path(path).read_bytes()
    except OSError as exc:
        raise ValidationError(f"cannot read {path}: {exc}") from exc
    if not data:
        return {"bytes": 0, "entropy": 0.0, "unique_values": 0}
    counts = Counter(data)
    length = len(data)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
    return {"bytes": length, "entropy": round(entropy, 6), "unique_values": len(counts)}


SECRET_PATTERNS = {
    "private-key": re.compile(r"BEGIN (?:RSA |OPENSSH )?PRIVATE KEY"),
    "github-token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "aws-access-key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "assignment": re.compile(r"""(?i)(?:password|secret|token|api[_-]?key)\s*[:=]\s*['"]?([^'"\s]{8,})"""),
}


def detect_secrets(text: str) -> list[dict[str, Any]]:
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        for kind, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append(
                    {"line": number, "type": kind, "preview": re.sub(r"(?<=[:=])[^\s]+", "[REDACTED]", line)[:120]}
                )
    return findings


def inspect_permissions(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    try:
        mode = target.stat().st_mode
    except OSError as exc:
        raise ValidationError(f"cannot inspect {target}: {exc}") from exc
    return {
        "path": str(target),
        "mode": oct(stat.S_IMODE(mode)),
        "owner_read": bool(mode & stat.S_IRUSR),
        "owner_write": bool(mode & stat.S_IWUSR),
        "owner_execute": bool(mode & stat.S_IXUSR),
        "world_writable": bool(mode & stat.S_IWOTH),
        "setuid": bool(mode & stat.S_ISUID),
        "setgid": bool(mode & stat.S_ISGID),
    }


def environment_secret_warnings() -> list[dict[str, str]]:
    words = ("PASSWORD", "TOKEN", "SECRET", "API_KEY", "PRIVATE_KEY", "CREDENTIAL")
    return [
        {"name": name, "value": "[REDACTED]"}
        for name in sorted(os.environ)
        if any(word in name.upper() for word in words)
    ]


def analyze_security_headers(headers: dict[str, str]) -> dict[str, Any]:
    normalized = {key.casefold(): value for key, value in headers.items()}
    expected = {
        "content-security-policy": "Restricts script and resource origins",
        "strict-transport-security": "Enforces HTTPS",
        "x-content-type-options": "Prevents MIME sniffing",
        "referrer-policy": "Limits referrer disclosure",
        "permissions-policy": "Restricts browser capabilities",
    }
    present = []
    missing = []
    for name, purpose in expected.items():
        (present if name in normalized else missing).append({"header": name, "purpose": purpose})
    return {"present": present, "missing": missing, "score": round(100 * len(present) / len(expected))}


def tls_certificate_information(hostname: str, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9.-]+", hostname) or ".." in hostname:
        raise ValidationError("invalid hostname")
    if port < 1 or port > 65535:
        raise ValidationError("port must be between 1 and 65535")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as raw:
            with context.wrap_socket(raw, server_hostname=hostname) as secured:
                certificate = secured.getpeercert()
    except (OSError, ssl.SSLError) as exc:
        raise ToolExecutionError(f"TLS inspection failed: {exc}") from exc
    subject = dict(item[0] for item in certificate.get("subject", ()))
    issuer = dict(item[0] for item in certificate.get("issuer", ()))
    return {
        "hostname": hostname,
        "subject": subject,
        "issuer": issuer,
        "serial_number": certificate.get("serialNumber"),
        "not_before": certificate.get("notBefore"),
        "not_after": certificate.get("notAfter"),
        "subject_alt_names": [value for kind, value in certificate.get("subjectAltName", ()) if kind == "DNS"],
    }
