from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from pyforge.models import Settings

DEFAULT_PATH = Path("config/settings.json")


def load_settings(path: Path = DEFAULT_PATH) -> Settings:
    try:
        return Settings.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, PydanticValidationError):
        return Settings()


def save_settings(settings: Settings, path: Path = DEFAULT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(settings.model_dump_json(indent=2) + "\n", encoding="utf-8")
