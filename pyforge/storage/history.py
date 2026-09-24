from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from pyforge.storage.database import DEFAULT_DATABASE, connect


class HistoryService:
    def __init__(self, path: Path = DEFAULT_DATABASE) -> None:
        self.path = path

    def record(self, tool: str, success: bool, duration_ms: float) -> None:
        with connect(self.path) as database:
            database.execute(
                "INSERT INTO history(tool,timestamp,success,duration_ms) VALUES(?,?,?,?)",
                (tool, datetime.now(timezone.utc).isoformat(), int(success), duration_ms),
            )

    def try_record(self, tool: str, success: bool, duration_ms: float) -> bool:
        """Record history when storage is available without masking tool output."""
        try:
            self.record(tool, success, duration_ms)
        except (OSError, sqlite3.Error):
            return False
        return True

    def list(self, limit: int = 100) -> list[dict[str, object]]:
        if limit < 1 or limit > 1000:
            raise ValueError("limit must be between 1 and 1000")
        with connect(self.path) as database:
            rows = database.execute(
                "SELECT tool,timestamp,success,duration_ms FROM history ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def clear(self) -> int:
        with connect(self.path) as database:
            count = database.execute("SELECT COUNT(*) FROM history").fetchone()[0]
            database.execute("DELETE FROM history")
        return count
