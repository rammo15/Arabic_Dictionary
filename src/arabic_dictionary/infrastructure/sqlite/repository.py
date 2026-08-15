from __future__ import annotations

from collections.abc import Iterable

from arabic_dictionary.domain import Entry, Sense
from arabic_dictionary.repository import DictionaryRepository
from arabic_dictionary.utils.normalizer import normalize

from .database import Database


class SQLiteRepository(DictionaryRepository):
    """SQLite implementation of DictionaryRepository."""

    def __init__(self, database: Database) -> None:
        self._database = database

    def save(self, entry: Entry) -> None:
        """Save an entry and its senses."""

        cursor = self._database.execute(
            """
            INSERT INTO entries (
                text,
                normalized_text,
                root,
                pronunciation,
                etymology,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entry.text,
                normalize(entry.text),
                entry.root,
                entry.pronunciation,
                entry.etymology,
                entry.source,
            ),
        )

        entry_id = cursor.lastrowid

        for sense in entry.senses:
            self._database.execute(
                """
                INSERT INTO senses (
                    entry_id,
                    meaning,
                    word_type,
                    notes
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    entry_id,
                    sense.meaning,
                    sense.word_type,
                    sense.notes,
                ),
            )

        self._database.connection.commit()

    def get(self, word: str) -> Entry | None:
        """Return an entry by its exact text."""

        cursor = self._database.execute(
            """
            SELECT
                id,
                text,
                root,
                pronunciation,
                etymology,
                source
            FROM entries
            WHERE text = ?
            LIMIT 1
            """,
            (word,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        entry_id = row[0]

        senses = self._get_senses(entry_id)

        return Entry(
            text=row[1],
            root=row[2],
            pronunciation=row[3],
            etymology=row[4],
            source=row[5],
            senses=senses,
        )

    def exists(self, word: str) -> bool:
        """Return True if an entry exists."""

        cursor = self._database.execute(
            """
            SELECT 1
            FROM entries
            WHERE text = ?
            LIMIT 1
            """,
            (word,),
        )

        return cursor.fetchone() is not None

    def delete(self, word: str) -> None:
        """Delete an entry."""

        self._database.execute(
            """
            DELETE FROM entries
            WHERE text = ?
            """,
            (word,),
        )

        self._database.connection.commit()

    def search(self, text: str) -> list[Entry]:
        """Search entries by text or root."""

        cursor = self._database.execute(
            """
            SELECT text
            FROM entries
            WHERE text LIKE ?
            OR root = ?
            ORDER BY text
            """,
            (f"%{text}%", text),
        )

        results: list[Entry] = []

        for row in cursor.fetchall():
            entry = self.get(row[0])

            if entry is not None:
                results.append(entry)

        return results

    def all(self) -> Iterable[Entry]:
        """Return all dictionary entries."""

        cursor = self._database.execute(
            """
            SELECT text
            FROM entries
            ORDER BY text
            """
        )

        for row in cursor.fetchall():
            entry = self.get(row[0])

            if entry is not None:
                yield entry

    def count(self) -> int:
        """Return the number of entries."""

        cursor = self._database.execute(
            "SELECT COUNT(*) FROM entries"
        )

        row = cursor.fetchone()

        return int(row[0])

    def clear(self) -> None:
        """Delete all entries."""

        self._database.execute("DELETE FROM entries")
        self._database.connection.commit()

    def _get_senses(self, entry_id: int) -> list[Sense]:
        """Load all senses belonging to an entry."""

        cursor = self._database.execute(
            """
            SELECT
                meaning,
                word_type,
                notes
            FROM senses
            WHERE entry_id = ?
            ORDER BY id
            """,
            (entry_id,),
        )

        return [
            Sense(
                meaning=row[0],
                word_type=row[1],
                notes=row[2],
            )
            for row in cursor.fetchall()
        ]