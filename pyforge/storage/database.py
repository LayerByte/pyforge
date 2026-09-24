from __future__ import annotations

import sqlite3
from pathlib import Path

DEFAULT_DATABASE = Path.home() / ".pyforge" / "history.db"


def connect(path: Path = DEFAULT_DATABASE) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("""CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        tool TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        success INTEGER NOT NULL,
        duration_ms REAL NOT NULL
    )""")
    return connection
