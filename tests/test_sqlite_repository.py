from arabic_dictionary.domain import Entry, Sense
from arabic_dictionary.infrastructure.sqlite.database import Database
from arabic_dictionary.infrastructure.sqlite.repository import SQLiteRepository


def create_repository() -> tuple[Database, SQLiteRepository]:
    db = Database(":memory:")
    db.initialize()

    return db, SQLiteRepository(db)


def test_empty_repository_count():
    db, repo = create_repository()

    assert repo.count() == 0

    db.close()


def test_empty_repository_exists():
    db, repo = create_repository()

    assert not repo.exists("كتاب")

    db.close()


def test_save_and_get():
    db, repo = create_repository()

    entry = Entry(
        text="كتاب",
        root="كتب",
        senses=[
            Sense(
                meaning="مؤلَّف يجمع مجموعة من الصفحات",
                word_type="اسم",
            )
        ],
    )

    repo.save(entry)

    result = repo.get("كتاب")

    assert result is not None
    assert result.text == "كتاب"
    assert result.root == "كتب"
    assert len(result.senses) == 1
    assert result.senses[0].meaning == "مؤلَّف يجمع مجموعة من الصفحات"

    db.close()


def test_delete():
    db, repo = create_repository()

    repo.save(Entry(text="كتاب"))

    assert repo.exists("كتاب")

    repo.delete("كتاب")

    assert not repo.exists("كتاب")
    assert repo.count() == 0

    db.close()


def test_search():
    db, repo = create_repository()

    repo.save(
        Entry(
            text="كتاب",
            root="كتب",
        )
    )

    repo.save(
        Entry(
            text="كاتب",
            root="كتب",
        )
    )

    repo.save(
        Entry(
            text="قلم",
            root="قلم",
        )
    )

    results = repo.search("كتب")

    words = [entry.text for entry in results]

    assert words == ["كاتب", "كتاب"]

    db.close()


def test_all():
    db, repo = create_repository()

    repo.save(Entry(text="كتاب"))
    repo.save(Entry(text="قلم"))

    results = list(repo.all())

    words = [entry.text for entry in results]

    assert words == ["قلم", "كتاب"]

    db.close()


def test_clear():
    db, repo = create_repository()

    repo.save(Entry(text="كتاب"))
    repo.save(Entry(text="قلم"))

    assert repo.count() == 2

    repo.clear()

    assert repo.count() == 0

    db.close()