from __future__ import annotations

from arabic_dictionary.domain import Entry
from arabic_dictionary.providers import Provider
from arabic_dictionary.repository import DictionaryRepository


class Dictionary:
    """High-level dictionary service.

    Looks up words in the repository first (cache-aside). On a miss,
    delegates to the provider, persists the result, and returns it.
    """

    def __init__(
        self,
        repository: DictionaryRepository,
        provider: Provider | None = None,
    ) -> None:
        self._repository = repository
        self._provider = provider

    def lookup(self, word: str) -> Entry | None:
        entry = self._repository.get(word)
        if entry is not None:
            return entry
        if self._provider is None:
            return None
        entry = self._provider.lookup(word)
        if entry is not None:
            self._repository.save(entry)
        return entry

    def exists(self, word: str) -> bool:
        return self._repository.exists(word)