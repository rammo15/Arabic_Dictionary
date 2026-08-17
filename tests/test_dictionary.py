from __future__ import annotations

from unittest.mock import MagicMock

from arabic_dictionary.application.dictionary import Dictionary
from arabic_dictionary.domain import Entry, Sense, WordType
from arabic_dictionary.providers import Provider
from arabic_dictionary.repository import InMemoryRepository

_KITAB = Entry(
    text="كتاب",
    source="wiktionary",
    root="كتب",
    senses=[Sense(meaning="كتاب يُقرأ.", word_type=WordType.NOUN)],
)


def _make_provider(result: Entry | None) -> Provider:
    mock = MagicMock(spec=Provider)
    mock.lookup.return_value = result
    return mock


# --- lookup: found in repository ---


def test_lookup_returns_entry_from_repository_when_present() -> None:
    repo = InMemoryRepository()
    repo.save(_KITAB)
    d = Dictionary(repository=repo)

    entry = d.lookup("كتاب")

    assert entry is _KITAB


def test_lookup_does_not_call_provider_when_entry_in_repository() -> None:
    repo = InMemoryRepository()
    repo.save(_KITAB)
    provider = _make_provider(_KITAB)
    d = Dictionary(repository=repo, provider=provider)

    d.lookup("كتاب")

    provider.lookup.assert_not_called()


# --- lookup: not in repository, provider consulted ---


def test_lookup_consults_provider_when_entry_not_in_repository() -> None:
    repo = InMemoryRepository()
    provider = _make_provider(_KITAB)
    d = Dictionary(repository=repo, provider=provider)

    entry = d.lookup("كتاب")

    assert entry is _KITAB
    provider.lookup.assert_called_once_with("كتاب")


def test_lookup_saves_entry_to_repository_after_provider_hit() -> None:
    repo = InMemoryRepository()
    provider = _make_provider(_KITAB)
    d = Dictionary(repository=repo, provider=provider)

    d.lookup("كتاب")

    assert repo.exists("كتاب")


def test_lookup_subsequent_call_uses_cached_entry() -> None:
    repo = InMemoryRepository()
    provider = _make_provider(_KITAB)
    d = Dictionary(repository=repo, provider=provider)

    d.lookup("كتاب")
    d.lookup("كتاب")

    # Second call should be served from repository; provider called only once
    provider.lookup.assert_called_once()


# --- lookup: not found anywhere ---


def test_lookup_returns_none_when_not_found_anywhere() -> None:
    repo = InMemoryRepository()
    provider = _make_provider(None)
    d = Dictionary(repository=repo, provider=provider)

    assert d.lookup("غير_موجود") is None


def test_lookup_returns_none_without_provider_when_not_in_repository() -> None:
    repo = InMemoryRepository()
    d = Dictionary(repository=repo)

    assert d.lookup("كتاب") is None


# --- exists ---


def test_exists_returns_true_when_entry_in_repository() -> None:
    repo = InMemoryRepository()
    repo.save(_KITAB)
    d = Dictionary(repository=repo)

    assert d.exists("كتاب") is True


def test_exists_returns_false_when_entry_not_in_repository() -> None:
    repo = InMemoryRepository()
    d = Dictionary(repository=repo)

    assert d.exists("كتاب") is False
