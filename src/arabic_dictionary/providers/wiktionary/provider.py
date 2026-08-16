from __future__ import annotations

import requests

from arabic_dictionary.domain import Entry
from arabic_dictionary.utils.normalizer import normalize as _normalize

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
        try:
            data = self._client.get_page(word)
        except requests.RequestException:
            return None

        wikitext = self._parser.extract_wikitext(data)
        code = self._parser.parse(wikitext)

        arabic = self._parser.find_arabic_section(code)
        if arabic is None:
            return None

        raw_root = self._parser.extract_root(arabic)
        entry = Entry(
            text=_normalize(word),
            source=self.name,
            root=_normalize(raw_root) if raw_root is not None else None,
        )

        for section in self._parser.extract_pos_sections(arabic):
            pos = self._parser.extract_part_of_speech(section)
            word_type = self._mapper.map_word_type(pos)
            raw_senses = self._parser.extract_senses(section)
            raw_synonyms = self._parser.extract_synonyms(section)
            raw_antonyms = self._parser.extract_antonyms(section)
            entry.senses.extend(
                self._mapper.map_senses(raw_senses, word_type, raw_synonyms, raw_antonyms)
            )

        return entry
