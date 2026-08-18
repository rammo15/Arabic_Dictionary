from __future__ import annotations

from unittest.mock import patch

from arabic_dictionary.providers.wiktionary import WiktionaryProvider
from arabic_dictionary.providers.wiktionary.parser import WiktionaryParser

_DISAMBIGUATION_WIKITEXT = """\
{{توضيح}}
هل تقصد:
* [[قَلَمَ]]
* [[قَلَّمَ]]
* [[قَلَمَ|قَلَم]]

[[تصنيف:مفردات بلا تشكيل]]
"""

_REAL_ENTRY_WIKITEXT = """\
==العربية==

{{جذر|ق|ل|م}}

===اسم===
{{ج|أقلام}}
# أداة للكتابة.
"""

_ANOTHER_DISAMBIGUATION = """\
{{توضيح}}
* [[أ]]
* [[ب]]
"""


class TestIsDisambiguationPage:
    def test_returns_true_for_disambiguation_page(self) -> None:
        parser = WiktionaryParser()
        code = parser.parse(_DISAMBIGUATION_WIKITEXT)
        assert parser.is_disambiguation_page(code) is True

    def test_returns_false_for_real_entry(self) -> None:
        parser = WiktionaryParser()
        code = parser.parse(_REAL_ENTRY_WIKITEXT)
        assert parser.is_disambiguation_page(code) is False


class TestExtractDisambiguationLinks:
    def test_extracts_link_targets(self) -> None:
        parser = WiktionaryParser()
        code = parser.parse(_DISAMBIGUATION_WIKITEXT)
        links = parser.extract_disambiguation_links(code)
        assert "قَلَمَ" in links
        assert "قَلَّمَ" in links

    def test_excludes_category_links(self) -> None:
        parser = WiktionaryParser()
        code = parser.parse(_DISAMBIGUATION_WIKITEXT)
        links = parser.extract_disambiguation_links(code)
        assert not any("تصنيف:" in link for link in links)
        assert not any("ملف:" in link for link in links)

    def test_no_duplicates(self) -> None:
        parser = WiktionaryParser()
        code = parser.parse(_DISAMBIGUATION_WIKITEXT)
        links = parser.extract_disambiguation_links(code)
        assert len(links) == len(set(links))


class TestProviderDisambiguation:
    def test_follows_first_valid_link(self) -> None:
        provider = WiktionaryProvider()

        def fake_get_page(title: str) -> dict:
            if title == "قلم":
                return {"parse": {"wikitext": {"*": _DISAMBIGUATION_WIKITEXT}}}
            return {"parse": {"wikitext": {"*": _REAL_ENTRY_WIKITEXT}}}

        with patch.object(provider._client, "get_page", side_effect=fake_get_page):
            entry = provider.lookup("قلم")

        assert entry is not None
        assert len(entry.senses) >= 1

    def test_returns_none_when_all_disambiguation_links_fail(self) -> None:
        provider = WiktionaryProvider()

        def fake_get_page(title: str) -> dict:
            # Every page is a disambiguation or has no Arabic section
            return {"parse": {"wikitext": {"*": _ANOTHER_DISAMBIGUATION}}}

        with patch.object(provider._client, "get_page", side_effect=fake_get_page):
            entry = provider.lookup("قلم")

        assert entry is None

    def test_skips_nested_disambiguation_links(self) -> None:
        provider = WiktionaryProvider()
        calls: list[str] = []

        def fake_get_page(title: str) -> dict:
            calls.append(title)
            if title == "قلم":
                return {"parse": {"wikitext": {"*": _DISAMBIGUATION_WIKITEXT}}}
            if title == "قَلَمَ":
                # First link is another disambiguation — should skip
                return {"parse": {"wikitext": {"*": _ANOTHER_DISAMBIGUATION}}}
            # Second link resolves
            return {"parse": {"wikitext": {"*": _REAL_ENTRY_WIKITEXT}}}

        with patch.object(provider._client, "get_page", side_effect=fake_get_page):
            entry = provider.lookup("قلم")

        assert entry is not None
        assert len(calls) >= 3  # original + at least 2 links tried
