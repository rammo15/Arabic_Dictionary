from arabic_dictionary.domain import Entry
from arabic_dictionary.repository import InMemoryRepository


def test_save():

    repo = InMemoryRepository()

    repo.save(Entry(text="كتاب"))

    assert repo.exists("كتاب")


def test_get():

    repo = InMemoryRepository()

    entry = Entry(text="قلم")

    repo.save(entry)

    assert repo.get("قلم") is entry


def test_count():

    repo = InMemoryRepository()

    repo.save(Entry(text="كتاب"))
    repo.save(Entry(text="قلم"))

    assert repo.count() == 2


def test_delete():

    repo = InMemoryRepository()

    repo.save(Entry(text="كتاب"))

    repo.delete("كتاب")

    assert not repo.exists("كتاب")


def test_clear():

    repo = InMemoryRepository()

    repo.save(Entry(text="كتاب"))
    repo.save(Entry(text="قلم"))

    repo.clear()

    assert repo.count() == 0
