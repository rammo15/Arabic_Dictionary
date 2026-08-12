from __future__ import annotations

from arabic_dictionary.domain import Entry
from arabic_dictionary.repository import DictionaryRepository


class Dictionary:
    """High-level dictionary service."""

    def __init__(self, repository: DictionaryRepository):
        self._repository = repository

        self.providers: list[DictionaryRepository] = []

    def add_provider(self, provider: DictionaryRepository):

        self.providers.append(provider)

    def lookup(self, word: str) -> Entry | None:
        return self._repository.get(word)

    def exists(self, word: str) -> bool:
        return self._repository.exists(word)

    def provider_names(self):

        return [p.name for p in self.providers]
