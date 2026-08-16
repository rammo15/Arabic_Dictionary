from __future__ import annotations

from arabic_dictionary.domain import Sense, WordType
from arabic_dictionary.utils.normalizer import normalize as _normalize

from .parser import ParsedSense

_WORD_TYPE_MAP: dict[str, WordType] = {
    "اسم": WordType.NOUN,
    "الاسم": WordType.NOUN,
    "فعل": WordType.VERB,
    "الفعل": WordType.VERB,
    "صفة": WordType.ADJECTIVE,
    "الصفة": WordType.ADJECTIVE,
    "ظرف": WordType.ADVERB,
    "حرف": WordType.PARTICLE,
    "ضمير": WordType.PRONOUN,
    "جملة": WordType.PHRASE,
}


class WiktionaryMapper:
    """Map parsed Wiktionary data into domain models."""

    def map_word_type(self, pos: str) -> WordType | None:
        return _WORD_TYPE_MAP.get(pos)

    def map_senses(
        self, senses: list[ParsedSense], word_type: WordType | None = None
    ) -> list[Sense]:
        return [
            Sense(
                meaning=_normalize(s.meaning),
                word_type=word_type,
                examples=[_normalize(e) for e in s.examples],
            )
            for s in senses
        ]
