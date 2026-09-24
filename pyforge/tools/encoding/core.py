from __future__ import annotations

import base64
import binascii
import html
from urllib.parse import quote, unquote

from pyforge.errors import ValidationError


def base64_encode(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def base64_decode(value: str) -> str:
    try:
        return base64.b64decode(value, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise ValidationError(f"invalid Base64 input: {exc}") from exc


def url_encode(text: str) -> str:
    return quote(text, safe="")


def url_decode(text: str) -> str:
    return unquote(text, errors="strict")


def hex_encode(text: str) -> str:
    return text.encode("utf-8").hex()


def hex_decode(value: str) -> str:
    try:
        return bytes.fromhex(value).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValidationError(f"invalid hexadecimal input: {exc}") from exc


def html_escape(text: str) -> str:
    return html.escape(text, quote=True)


def html_unescape(text: str) -> str:
    return html.unescape(text)
