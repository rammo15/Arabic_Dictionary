from __future__ import annotations

import pytest

from arabic_dictionary.providers.wiktionary import WiktionaryProvider


@pytest.mark.network
@pytest.mark.parametrize("word", ["كتاب"])
def test_lookup_live_wiktionary(word: str) -> None:
    provider = WiktionaryProvider()

    entry = provider.lookup(word)

    assert entry is not None
    assert entry.text == word
    assert len(entry.senses) >= 1
    assert all(s.meaning for s in entry.senses)
    assert entry.root == "كتب"
