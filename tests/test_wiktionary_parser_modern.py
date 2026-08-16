from __future__ import annotations

from pathlib import Path

from arabic_dictionary.providers.wiktionary.parser import WiktionaryParser

_FIXTURE = (Path(__file__).parent / "fixtures" / "kitab_wikitext.txt").read_text()


def test_find_arabic_section_modern_format() -> None:
    parser = WiktionaryParser()

    code = parser.parse(_FIXTURE)
    section = parser.find_arabic_section(code)

    assert section is not None


def test_find_meanings_section() -> None:
    parser = WiktionaryParser()

    code = parser.parse(_FIXTURE)
    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    meanings = parser.find_meanings_section(arabic)

    assert meanings is not None
    assert "# " in str(meanings)


def test_extract_senses_from_meanings_section() -> None:
    parser = WiktionaryParser()

    code = parser.parse(_FIXTURE)
    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    meanings = parser.find_meanings_section(arabic)
    assert meanings is not None

    senses = parser.extract_senses(meanings)

    assert len(senses) == 3
    assert "كُتِبَ" in senses[0].meaning or "كتب" in senses[0].meaning
    assert senses[1].examples != []


def test_find_meanings_section_returns_none_when_absent() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==

===اسم===
# كتاب.
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    assert parser.find_meanings_section(arabic) is None
