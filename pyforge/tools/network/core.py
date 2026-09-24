from __future__ import annotations

import ipaddress
import socket
import time
from typing import Any
from urllib.parse import urlparse

import httpx
import psutil

from pyforge.errors import ToolExecutionError, ValidationError


def dns_lookup(hostname: str) -> list[str]:
    if not hostname.strip():
        raise ValidationError("hostname cannot be empty")
    try:
        return sorted({item[4][0] for item in socket.getaddrinfo(hostname, None)})
    except socket.gaierror as exc:
        raise ToolExecutionError(f"DNS lookup failed: {exc}") from exc


def reverse_dns_lookup(address: str) -> str:
    try:
        ipaddress.ip_address(address)
    except ValueError as exc:
        raise ValidationError(f"invalid IP address: {address}") from exc
    try:
        return socket.gethostbyaddr(address)[0]
    except socket.herror as exc:
        raise ToolExecutionError(f"reverse DNS lookup failed: {exc}") from exc


def local_ip_information() -> dict[str, Any]:
    hostname = socket.gethostname()
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(hostname, None)})
    return {"hostname": hostname, "addresses": addresses}


def network_interfaces() -> list[dict[str, Any]]:
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    result = []
    for name, items in sorted(addresses.items()):
        result.append(
            {
                "name": name,
                "up": stats.get(name).isup if name in stats else None,
                "addresses": [
                    {"family": str(item.family), "address": item.address, "netmask": item.netmask} for item in items
                ],
            }
        )
    return result


def public_ip(timeout: float = 5.0, client: httpx.Client | None = None) -> str:
    if timeout <= 0:
        raise ValidationError("timeout must be positive")
    owned = client is None
    active = client or httpx.Client(timeout=timeout)
    try:
        response = active.get("https://api.ipify.org", params={"format": "json"})
        response.raise_for_status()
        value = response.json()["ip"]
        ipaddress.ip_address(value)
        return value
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        raise ToolExecutionError(f"public IP lookup failed: {exc}") from exc
    finally:
        if owned:
            active.close()


def http_headers(url: str, timeout: float = 5.0, client: httpx.Client | None = None) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError("a valid HTTP(S) URL is required")
    owned = client is None
    active = client or httpx.Client(timeout=timeout, follow_redirects=True)
    try:
        response = active.head(url)
        response.raise_for_status()
        return dict(response.headers)
    except httpx.HTTPError as exc:
        raise ToolExecutionError(f"header request failed: {exc}") from exc
    finally:
        if owned:
            active.close()


def http_status(url: str, timeout: float = 5.0, client: httpx.Client | None = None) -> dict[str, Any]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError("a valid HTTP(S) URL is required")
    owned = client is None
    active = client or httpx.Client(timeout=timeout, follow_redirects=True)
    try:
        started = time.perf_counter()
        response = active.get(url)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "status": response.status_code,
            "ok": response.is_success,
            "elapsed_ms": elapsed_ms,
            "url": str(response.url),
        }
    except httpx.HTTPError as exc:
        raise ToolExecutionError(f"status request failed: {exc}") from exc
    finally:
        if owned:
            active.close()


def parse_url(value: str) -> dict[str, Any]:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValidationError("a valid HTTP(S) URL is required")
    return {
        "scheme": parsed.scheme,
        "hostname": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path or "/",
        "query": parsed.query,
        "fragment": parsed.fragment,
        "username_present": parsed.username is not None,
    }
