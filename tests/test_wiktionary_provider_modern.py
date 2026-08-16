from __future__ import annotations

from pathlib import Path

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
