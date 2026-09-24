from __future__ import annotations

import difflib
import re
import unicodedata
from collections import Counter

from pyforge.errors import ValidationError


def text_statistics(text: str) -> dict[str, object]:
    words = re.findall(r"\b[^\W_]+(?:['’-][^\W_]+)*\b", text, flags=re.UNICODE)
    sentences = re.findall(r"[^.!?]+[.!?]+|[^.!?\s][^.!?]*$", text.strip(), flags=re.UNICODE)
    paragraphs = [block for block in re.split(r"(?:\r?\n){2,}", text.strip()) if block.strip()]
    unique_words = {word.casefold() for word in words}
    characters = len(text)
    non_whitespace = sum(not char.isspace() for char in text)
    return {
        "characters": characters,
        "non_whitespace_characters": non_whitespace,
        "words": len(words),
        "unique_words": len(unique_words),
        "lines": line_count(text),
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "average_word_length": round(sum(len(word) for word in words) / len(words), 2) if words else 0.0,
        "reading_time_minutes": round(len(words) / 200, 2) if words else 0.0,
    }


def word_count(text: str) -> int:
    return len(re.findall(r"\b[^\W_]+(?:['’-][^\W_]+)*\b", text, flags=re.UNICODE))


def line_count(text: str) -> int:
    return len(text.splitlines()) if text else 0


def character_count(text: str, include_whitespace: bool = True) -> int:
    return len(text) if include_whitespace else sum(not char.isspace() for char in text)


def duplicate_lines(text: str, ignore_blank: bool = True) -> dict[str, int]:
    lines = [line for line in text.splitlines() if line.strip() or not ignore_blank]
    return {line: count for line, count in Counter(lines).items() if count > 1}


def text_difference(before: str, after: str, before_name: str = "before", after_name: str = "after") -> str:
    return "".join(
        difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile=before_name, tofile=after_name)
    )


def clean_whitespace(text: str, max_blank_lines: int = 1) -> str:
    if max_blank_lines < 0:
        raise ValidationError("max_blank_lines cannot be negative")
    output = []
    blanks = 0
    for line in text.splitlines():
        cleaned = line.rstrip()
        if cleaned:
            blanks = 0
            output.append(cleaned)
        else:
            blanks += 1
            if blanks <= max_blank_lines:
                output.append("")
    return "\n".join(output).strip("\n") + ("\n" if text else "")


def convert_case(text: str, mode: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text))
    if mode == "upper":
        return text.upper()
    if mode == "lower":
        return text.lower()
    if mode == "title":
        return text.title()
    if mode == "snake":
        return "_".join(word.lower() for word in words)
    if mode == "kebab":
        return "-".join(word.lower() for word in words)
    if mode == "camel":
        return (words[0].lower() + "".join(w.title() for w in words[1:])) if words else ""
    raise ValidationError(f"unsupported case mode: {mode}")


def slugify(text: str, separator: str = "-") -> str:
    if separator not in {"-", "_"}:
        raise ValidationError("separator must be '-' or '_'")
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[A-Za-z0-9]+", ascii_text.casefold())
    return separator.join(words)


def sort_text(text: str, reverse: bool = False, unique: bool = False, case_sensitive: bool = False) -> str:
    lines = text.splitlines()
    if unique:
        lines = list(dict.fromkeys(lines))
    lines.sort(key=None if case_sensitive else str.casefold, reverse=reverse)
    return "\n".join(lines)


def search_text(text: str, query: str, case_sensitive: bool = False) -> list[dict[str, object]]:
    if not query:
        raise ValidationError("query cannot be empty")
    needle = query if case_sensitive else query.casefold()
    result = []
    for number, line in enumerate(text.splitlines(), 1):
        haystack = line if case_sensitive else line.casefold()
        if needle in haystack:
            result.append({"line": number, "text": line})
    return result


def regex_test(pattern: str, text: str, flags: int = 0) -> list[dict[str, object]]:
    try:
        expression = re.compile(pattern, flags)
    except re.error as exc:
        raise ValidationError(f"invalid regular expression: {exc}") from exc
    return [
        {"value": match.group(0), "start": match.start(), "end": match.end(), "groups": list(match.groups())}
        for match in expression.finditer(text)
    ]
