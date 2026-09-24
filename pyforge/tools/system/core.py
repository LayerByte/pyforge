from __future__ import annotations

import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil


def cpu_information() -> dict[str, Any]:
    frequency = psutil.cpu_freq()
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(),
        "usage_percent": psutil.cpu_percent(interval=0.0),
        "frequency_mhz": frequency.current if frequency else None,
        "processor": platform.processor(),
    }


def memory_information() -> dict[str, Any]:
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "percent": memory.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_percent": swap.percent,
    }


def disk_information() -> list[dict[str, Any]]:
    result = []
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except (PermissionError, OSError):
            continue
        result.append(
            {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            }
        )
    return result


def operating_system_information() -> dict[str, str]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "node": platform.node(),
        "platform": platform.platform(),
    }


def environment_information() -> dict[str, str]:
    sensitive = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASS", "CREDENTIAL")
    return {
        key: ("[REDACTED]" if any(word in key.upper() for word in sensitive) else value)
        for key, value in sorted(os.environ.items())
    }


def process_viewer(limit: int = 50) -> list[dict[str, Any]]:
    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")
    result = []
    for process in psutil.process_iter(["pid", "name", "username", "memory_percent", "cpu_percent"]):
        try:
            result.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(result, key=lambda row: row.get("memory_percent") or 0, reverse=True)[:limit]


def listening_ports() -> list[dict[str, Any]]:
    result = []
    try:
        connections = psutil.net_connections(kind="inet")
    except (psutil.AccessDenied, OSError):
        return result
    for connection in connections:
        if connection.status == psutil.CONN_LISTEN and connection.laddr:
            result.append(
                {
                    "address": connection.laddr.ip,
                    "port": connection.laddr.port,
                    "pid": connection.pid,
                    "family": str(connection.family),
                }
            )
    return sorted(result, key=lambda row: (row["port"], row["address"]))


def system_uptime() -> dict[str, Any]:
    boot = psutil.boot_time()
    seconds = max(0, int(datetime.now(timezone.utc).timestamp() - boot))
    return {
        "boot_time": datetime.fromtimestamp(boot, timezone.utc).isoformat(),
        "seconds": seconds,
        "days": seconds // 86400,
        "hours": (seconds % 86400) // 3600,
    }


def python_environment_information() -> dict[str, Any]:
    return {
        "version": sys.version,
        "executable": sys.executable,
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
        "virtual_environment": sys.prefix != sys.base_prefix,
        "path": [str(Path(item)) for item in sys.path],
    }
