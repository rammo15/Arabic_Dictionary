import sqlite3

from arabic_dictionary.infrastructure.sqlite.database import Database


def test_database_initialization():

    db = Database(":memory:")

    db.initialize()

    cursor = db.connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = {
        row[0]
        for row in cursor.fetchall()
    }

    assert "entries" in tables
    assert "senses" in tables
    assert "examples" in tables
    assert "relations" in tables

    db.close()