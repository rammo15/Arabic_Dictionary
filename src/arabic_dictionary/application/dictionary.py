from __future__ import annotations

from arabic_dictionary.domain import Entry
from arabic_dictionary.providers import Provider
from arabic_dictionary.repository import DictionaryRepository


class Dictionary:
    """High-level dictionary service."""

    def __init__(self, repository: DictionaryRepository) -> None:
        self._repository = repository
        self.providers: list[Provider] = []

    def add_provider(self, provider: Provider) -> None:
        self.providers.append(provider)

    def lookup(self, word: str) -> Entry | None:
        return self._repository.get(word)

    def exists(self, word: str) -> bool:
        return self._repository.exists(word)

    def provider_names(self) -> list[str]:
        return [p.name for p in self.providers]