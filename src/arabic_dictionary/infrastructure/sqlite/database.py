from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    """SQLite database manager."""

    def __init__(self, path: str | Path):

        self.path = str(path)

        self.connection = sqlite3.connect(self.path)

        self.connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

    def initialize(self) -> None:
        """Create all database tables."""

        schema = (
            Path(__file__)
            .with_name("schema.sql")
            .read_text(encoding="utf-8")
        )

        self.connection.executescript(schema)

        self.connection.commit()

    def close(self) -> None:

        self.connection.close()

    def execute(self, sql: str, parameters: tuple = ()):
        return self._connection.execute(sql, parameters)

    def executescript(self, script: str):
        return self._connection.executescript(script)