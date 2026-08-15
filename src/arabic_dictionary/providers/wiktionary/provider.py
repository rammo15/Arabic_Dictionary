from __future__ import annotations

from arabic_dictionary.domain import Entry

from ..base import Provider


class WiktionaryProvider(Provider):
    """Wiktionary dictionary provider."""

    @property
    def name(self) -> str:
        return "wiktionary"

    def lookup(self, word: str) -> Entry | None:
        raise NotImplementedError("WiktionaryProvider is not implemented yet.")