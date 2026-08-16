from __future__ import annotations

from unittest.mock import patch

import requests

from arabic_dictionary.domain import WordType
from arabic_dictionary.providers.wiktionary import (
    MediaWikiClient,
    WiktionaryMapper,
    WiktionaryParser,
    WiktionaryProvider,
)

_ARABIC_WIKITEXT = """
==العربية==


{{جذر|ك|ت|ب}}


===اسم===
# كتاب يُقرأ.
#: هذا كتابٌ مفيد.
# مؤلف.
#: قرأتُ كتابًا جديدًا.

====مرادفات====
* سِفْر
* مُجَلَّد

====أضداد====
* مَقَالٌ
"""


class FakeClient(MediaWikiClient):
    def get_page(self, title: str) -> dict:  # type: ignore[override]
        return {"parse": {"wikitext": {"*": _ARABIC_WIKITEXT}}}


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
        return_value={"parse": {"wikitext": {"*": _ARABIC_WIKITEXT}}},
    ):
        entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.text == "كتاب"
    assert entry.source == "wiktionary"


def test_lookup_returns_entry() -> None:
    provider = WiktionaryProvider(
        client=FakeClient(),
        parser=WiktionaryParser(),
        mapper=WiktionaryMapper(),
    )

    entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.text == "كتاب"
    assert entry.root == "كتب"
    assert len(entry.senses) == 2
    assert entry.senses[0].meaning == "كتاب يقرا."
    assert entry.senses[0].word_type == WordType.NOUN
    assert entry.senses[0].examples == ["هذا كتاب مفيد."]
    assert entry.senses[1].meaning == "مؤلف."
    assert entry.senses[1].word_type == WordType.NOUN
    assert entry.senses[1].examples == ["قرات كتابا جديدا."]
    assert entry.senses[0].synonyms == ["سفر", "مجلد"]
    assert entry.senses[1].synonyms == ["سفر", "مجلد"]
    assert entry.senses[0].antonyms == ["مقال"]
    assert entry.senses[1].antonyms == ["مقال"]


def test_lookup_returns_none_on_connection_error() -> None:
    provider = WiktionaryProvider()

    with patch.object(
        provider._client,
        "get_page",
        side_effect=requests.exceptions.ConnectionError,
    ):
        assert provider.lookup("كتاب") is None


def test_lookup_returns_none_on_timeout() -> None:
    provider = WiktionaryProvider()

    with patch.object(
        provider._client,
        "get_page",
        side_effect=requests.exceptions.Timeout,
    ):
        assert provider.lookup("كتاب") is None


def test_lookup_returns_none_on_http_error() -> None:
    provider = WiktionaryProvider()

    with patch.object(
        provider._client,
        "get_page",
        side_effect=requests.exceptions.HTTPError,
    ):
        assert provider.lookup("كتاب") is None
