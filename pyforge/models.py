from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class ExportFormat(StrEnum):
    TXT = "txt"
    JSON = "json"
    CSV = "csv"


class Settings(BaseModel):
    theme: str = "dark"
    history_enabled: bool = True
    default_export_format: ExportFormat = ExportFormat.JSON
    http_timeout: float = Field(default=5.0, ge=0.1, le=60.0)
    show_advanced_information: bool = False


class ToolSpec(BaseModel):
    name: str
    category: str
    title: str
    description: str
    import_path: str
    sensitive_input: bool = False
