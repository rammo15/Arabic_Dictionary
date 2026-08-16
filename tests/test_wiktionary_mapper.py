from __future__ import annotations

from arabic_dictionary.domain import WordType
from arabic_dictionary.providers.wiktionary.mapper import WiktionaryMapper
from arabic_dictionary.providers.wiktionary.parser import ParsedSense


def test_map_word_type_known() -> None:
    mapper = WiktionaryMapper()

    assert mapper.map_word_type("اسم") == WordType.NOUN
    assert mapper.map_word_type("فعل") == WordType.VERB
    assert mapper.map_word_type("صفة") == WordType.ADJECTIVE


def test_map_word_type_unknown() -> None:
    mapper = WiktionaryMapper()

    assert mapper.map_word_type("شيء_غير_معروف") is None


def test_map_senses() -> None:
    mapper = WiktionaryMapper()

    senses = mapper.map_senses(
        [
            ParsedSense(meaning="كتاب"),
            ParsedSense(meaning="مؤلف"),
        ]
    )

    assert len(senses) == 2
    assert senses[0].meaning == "كتاب"
    assert senses[1].meaning == "مؤلف"


def test_map_senses_with_synonyms() -> None:
    mapper = WiktionaryMapper()

    senses = mapper.map_senses(
        senses=[ParsedSense(meaning="كتاب")],
        synonyms=["سِفْر", "مُجَلَّد"],
    )

    assert senses[0].synonyms == ["سفر", "مجلد"]


def test_map_sense_normalizes_text() -> None:
    mapper = WiktionaryMapper()

    senses = mapper.map_senses(
        senses=[
            ParsedSense(
                meaning="كِتَابٌ",
                examples=["هٰذا كِتَابٌ"],
            )
        ],
        word_type=WordType.NOUN,
    )

    assert senses[0].meaning == "كتاب"
    assert senses[0].examples == ["هذا كتاب"]
