"""
In-memory repository.

Useful for tests.
"""

from __future__ import annotations

from arabic_dictionary.domain import Entry

from .base import DictionaryRepository


class InMemoryRepository(DictionaryRepository):
    def __init__(self):

        self._entries: dict[str, Entry] = {}

    def get(self, word: str) -> Entry | None:

        return self._entries.get(word)

    def save(self, entry: Entry) -> None:

        self._entries[entry.text] = entry

    def delete(self, word: str) -> None:

        self._entries.pop(word, None)

    def exists(self, word: str) -> bool:

        return word in self._entries

    def search(self, text: str) -> list[Entry]:

        return [entry for entry in self._entries.values() if text in entry.text]

    def all(self):

        return self._entries.values()

    def count(self) -> int:

        return len(self._entries)

    def clear(self):

        self._entries.clear()
