from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import Entry


class SQLiteStorage:

    def __init__(self, database: str | Path):

        self.database = Path(database)

        self.connection = sqlite3.connect(self.database)

        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries(

            text TEXT PRIMARY KEY,

            word_type TEXT,

            meaning TEXT,

            root TEXT,

            plural TEXT,

            singular TEXT,

            masculine TEXT,

            feminine TEXT,

            source TEXT

        );
        """)

        self.connection.commit()

    def exists(self, word: str):

        cursor = self.connection.execute(

            "SELECT 1 FROM entries WHERE text=?",

            (word,)

        )

        return cursor.fetchone() is not None

    def insert(self, entry: Entry):

        self.connection.execute("""

        INSERT OR REPLACE INTO entries

        VALUES(?,?,?,?,?,?,?,?,?)

        """, (

            entry.text,

            entry.word_type,

            entry.meaning,

            entry.root,

            entry.plural,

            entry.singular,

            entry.masculine,

            entry.feminine,

            entry.source

        ))

        self.connection.commit()

    def get(self, word: str):

        cursor = self.connection.execute(

            "SELECT * FROM entries WHERE text=?",

            (word,)

        )

        row = cursor.fetchone()

        if row is None:

            return None

        return Entry(

            text=row["text"],

            word_type=row["word_type"],

            meaning=row["meaning"],

            root=row["root"],

            plural=row["plural"],

            singular=row["singular"],

            masculine=row["masculine"],

            feminine=row["feminine"],

            source=row["source"]

        )

    def close(self):

        self.connection.close()
