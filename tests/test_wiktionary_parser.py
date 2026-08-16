from __future__ import annotations

import mwparserfromhell

from arabic_dictionary.providers.wiktionary.parser import ParsedSense, WiktionaryParser


def test_parse_empty_text() -> None:
    parser = WiktionaryParser()

    code = parser.parse("")

    assert str(code) == ""


def test_parse_returns_wikicode() -> None:
    parser = WiktionaryParser()

    code = parser.parse("==العربية==")

    assert isinstance(code, mwparserfromhell.wikicode.Wikicode)


def test_find_arabic_section() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==English==
Text


==العربية==
===اسم===
# كتاب


==Français==
Texte
"""
    )

    section = parser.find_arabic_section(code)

    assert section is not None
    assert "===اسم===" in str(section)
    assert "# كتاب" in str(section)


def test_find_arabic_section_with_language_template() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
=={{اللغة|إنجليزية}}==
Text


=={{اللغة|عربية}}==
===اسم===
# كتاب


=={{اللغة|فرنسية}}==
Texte
"""
    )

    section = parser.find_arabic_section(code)

    assert section is not None
    assert "===اسم===" in str(section)
    assert "# كتاب" in str(section)


def test_find_arabic_section_returns_none_for_non_arabic_template() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
=={{اللغة|إنجليزية}}==
===Noun===
# book
"""
    )

    assert parser.find_arabic_section(code) is None


def test_extract_pos_sections() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===اسم===
# كتاب


===فعل===
# كتب


===صفة===
# مكتوب
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    sections = parser.extract_pos_sections(arabic)

    assert len(sections) == 3

    assert str(sections[0].filter_headings()[0].title).strip() == "اسم"
    assert str(sections[1].filter_headings()[0].title).strip() == "فعل"
    assert str(sections[2].filter_headings()[0].title).strip() == "صفة"


def test_extract_senses() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===اسم===
# كتاب يُقرأ.
# مؤلف.
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos = parser.extract_pos_sections(arabic)[0]

    senses = parser.extract_senses(pos)

    assert len(senses) == 2
    assert senses[0].meaning == "كتاب يُقرأ."
    assert senses[1].meaning == "مؤلف."


def test_extract_senses_with_examples() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===اسم===
# كتاب يُقرأ.
#: هذا كتابٌ مفيد.
# مؤلف.
#: قرأتُ كتابًا جديدًا.
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos = parser.extract_pos_sections(arabic)[0]
    senses = parser.extract_senses(pos)

    assert len(senses) == 2

    assert senses[0] == ParsedSense(
        meaning="كتاب يُقرأ.",
        examples=["هذا كتابٌ مفيد."],
    )
    assert senses[1] == ParsedSense(
        meaning="مؤلف.",
        examples=["قرأتُ كتابًا جديدًا."],
    )


def test_extract_root() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


{{جذر|ك|ت|ب}}


===اسم===
# كتاب.
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    assert parser.extract_root(arabic) == "كتب"


def test_extract_root_returns_none_when_absent() -> None:
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

    assert parser.extract_root(arabic) is None


def test_extract_part_of_speech() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===اسم===
# كتاب
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos_section = parser.extract_pos_sections(arabic)[0]

    assert parser.extract_part_of_speech(pos_section) == "اسم"


def test_extract_synonyms() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===اسم===
# كتاب.

====مرادفات====
* سِفْر
* مُجَلَّد
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos_section = parser.extract_pos_sections(arabic)[0]

    assert parser.extract_synonyms(pos_section) == ["سِفْر", "مُجَلَّد"]


def test_extract_synonyms_returns_empty_when_absent() -> None:
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

    pos_section = parser.extract_pos_sections(arabic)[0]

    assert parser.extract_synonyms(pos_section) == []


def test_extract_antonyms() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===صفة===
# كبير.

====أضداد====
* صغير
* ضئيل
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos_section = parser.extract_pos_sections(arabic)[0]

    assert parser.extract_antonyms(pos_section) == ["صغير", "ضئيل"]


def test_extract_antonyms_returns_empty_when_absent() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===صفة===
# كبير.
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos_section = parser.extract_pos_sections(arabic)[0]

    assert parser.extract_antonyms(pos_section) == []


def test_extract_plural() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===اسم===
{{ج|كُتُب}}
# كتاب يُقرأ.
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos_section = parser.extract_pos_sections(arabic)[0]

    assert parser.extract_plural(pos_section) == "كُتُب"


def test_extract_plural_returns_none_when_absent() -> None:
    parser = WiktionaryParser()

    code = parser.parse(
        """
==العربية==


===اسم===
# كتاب يُقرأ.
"""
    )

    arabic = parser.find_arabic_section(code)
    assert arabic is not None

    pos_section = parser.extract_pos_sections(arabic)[0]

    assert parser.extract_plural(pos_section) is None


def test_extract_wikitext() -> None:
    parser = WiktionaryParser()

    data = {
        "parse": {
            "wikitext": {
                "*": "==العربية==\n===اسم===\n# كتاب"
            }
        }
    }

    assert (
        parser.extract_wikitext(data)
        == "==العربية==\n===اسم===\n# كتاب"
    )
