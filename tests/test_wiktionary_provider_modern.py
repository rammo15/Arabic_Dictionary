from __future__ import annotations

from pathlib import Path

from arabic_dictionary.domain import WordType
from arabic_dictionary.providers.wiktionary import (
    MediaWikiClient,
    WiktionaryMapper,
    WiktionaryParser,
    WiktionaryProvider,
)

_KITAB_WIKITEXT = (Path(__file__).parent / "fixtures" / "kitab_wikitext.txt").read_text()


class FakeModernClient(MediaWikiClient):
    def get_page(self, title: str) -> dict:  # type: ignore[override]
        return {"parse": {"wikitext": {"*": _KITAB_WIKITEXT}}}


def test_lookup_supports_modern_wiktionary_page() -> None:
    provider = WiktionaryProvider(
        client=FakeModernClient(),
        parser=WiktionaryParser(),
        mapper=WiktionaryMapper(),
    )

    entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.text == "كتاب"
    assert len(entry.senses) >= 1
    assert entry.senses[0].meaning.startswith("الشيء")


def test_lookup_modern_returns_noun_word_type() -> None:
    provider = WiktionaryProvider(
        client=FakeModernClient(),
        parser=WiktionaryParser(),
        mapper=WiktionaryMapper(),
    )

    entry = provider.lookup("كتاب")

    assert entry is not None
    assert len(entry.senses) >= 1
    assert entry.senses[0].word_type == WordType.NOUN


def test_lookup_modern_page_sets_root() -> None:
    provider = WiktionaryProvider(
        client=FakeModernClient(),
        parser=WiktionaryParser(),
        mapper=WiktionaryMapper(),
    )

    entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.root == "كتب"


def test_lookup_modern_page_sets_plural() -> None:
    provider = WiktionaryProvider(
        client=FakeModernClient(),
        parser=WiktionaryParser(),
        mapper=WiktionaryMapper(),
    )

    entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.plural == "كتب"
