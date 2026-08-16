from __future__ import annotations

from arabic_dictionary.domain import Sense


class WiktionaryMapper:
    """Map parsed Wiktionary data into domain models."""

    def map_senses(self, senses: list[str]) -> list[Sense]:
        return [Sense(meaning=text) for text in senses]
