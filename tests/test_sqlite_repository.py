from arabic_dictionary.infrastructure.sqlite.database import Database
from arabic_dictionary.infrastructure.sqlite.repository import SQLiteRepository


def test_empty_repository_count():
    db = Database(":memory:")
    db.initialize()

    repo = SQLiteRepository(db)

    assert repo.count() == 0

    db.close()


def test_empty_repository_exists():
    db = Database(":memory:")
    db.initialize()

    repo = SQLiteRepository(db)

    assert not repo.exists("كتاب")

    db.close()
