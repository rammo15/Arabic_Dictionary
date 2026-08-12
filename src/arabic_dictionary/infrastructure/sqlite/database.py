from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    """SQLite database manager."""

    def __init__(self, path: str | Path):

        self.path = str(path)

        self._connection = sqlite3.connect(self.path)

        self._connection.execute("PRAGMA foreign_keys = ON;")

    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    def initialize(self) -> None:
        """Create all database tables."""

        schema = (
            Path(__file__)
            .with_name("schema.sql")
            .read_text(encoding="utf-8")
        )

        self._connection.executescript(schema)

        self._connection.commit()

    def execute(
        self,
        sql: str,
        parameters: tuple = (),
    ):
        return self._connection.execute(sql, parameters)

    def executescript(self, script: str):
        return self._connection.executescript(script)

    def close(self) -> None:
        self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()