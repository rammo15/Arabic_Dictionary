from __future__ import annotations

from arabic_dictionary.providers.wiktionary.mapper import WiktionaryMapper


def test_map_senses() -> None:
    mapper = WiktionaryMapper()

    senses = mapper.map_senses(
        [
            "كتاب يُقرأ.",
            "مؤلف.",
        ]
    )

    assert len(senses) == 2
    assert senses[0].meaning == "كتاب يُقرأ."
    assert senses[1].meaning == "مؤلف."
