from __future__ import annotations

from arabic_dictionary.domain import Entry

from ..base import Provider
from .client import MediaWikiClient
from .mapper import WiktionaryMapper
from .parser import WiktionaryParser


class WiktionaryProvider(Provider):
    """Wiktionary dictionary provider."""

    def __init__(
        self,
        client: MediaWikiClient | None = None,
        parser: WiktionaryParser | None = None,
        mapper: WiktionaryMapper | None = None,
    ) -> None:
        self._client = client or MediaWikiClient()
        self._parser = parser or WiktionaryParser()
        self._mapper = mapper or WiktionaryMapper()

    @property
    def name(self) -> str:
        return "wiktionary"

    def lookup(self, word: str) -> Entry | None:
        data = self._client.get_page(word)

        wikitext = self._parser.extract_wikitext(data)
        code = self._parser.parse(wikitext)

        arabic = self._parser.find_arabic_section(code)
        if arabic is None:
            return None

        entry = Entry(text=word, source=self.name)

        for section in self._parser.extract_pos_sections(arabic):
            raw_senses = self._parser.extract_senses(section)
            entry.senses.extend(self._mapper.map_senses(raw_senses))

        return entry
