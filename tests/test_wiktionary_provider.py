from __future__ import annotations

from unittest.mock import patch

from arabic_dictionary.providers.wiktionary.provider import WiktionaryProvider


def test_lookup_returns_none_when_page_does_not_exist() -> None:
    provider = WiktionaryProvider()

    with patch.object(
        provider._client,
        "get_page",
        return_value={"error": {"code": "missingtitle"}},
    ):
        assert provider.lookup("كلمةغيرموجودة") is None


def test_lookup_returns_entry_for_existing_page() -> None:
    provider = WiktionaryProvider()

    with patch.object(
        provider._client,
        "get_page",
        return_value={"parse": {"title": "كتاب", "wikitext": {"*": "..."}}},
    ):
        entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.text == "كتاب"
    assert entry.source == "wiktionary"