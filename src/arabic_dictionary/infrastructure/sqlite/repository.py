from __future__ import annotations

from arabic_dictionary.domain import Entry
from arabic_dictionary.repository import DictionaryRepository

from .database import Database


class SQLiteRepository(DictionaryRepository):
    """SQLite implementation of DictionaryRepository."""

    def __init__(self, database: Database):
        self._database = database

    def exists(self, word: str) -> bool:
        cursor = self._database.connection.execute(
            """
            SELECT 1
            FROM entries
            WHERE text = ?
            LIMIT 1
            """,
            (word,),
        )

        return cursor.fetchone() is not None

    def count(self) -> int:
        cursor = self._database.connection.execute(
            "SELECT COUNT(*) FROM entries"
        )

        return int(cursor.fetchone()[0])