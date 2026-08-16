from __future__ import annotations

from arabic_dictionary.domain import Entry

from ..base import Provider
from .client import MediaWikiClient


class WiktionaryProvider(Provider):
    """Wiktionary dictionary provider."""

    @property
    def name(self) -> str:
        return "wiktionary"

    def lookup(self, word: str) -> Entry | None:
        data = self._client.get_page(word)

        if "error" in data:
            return None

        return Entry(
            text=word,
            source=self.name,
        )

    def __init__(self) -> None:
        self._client = MediaWikiClient()