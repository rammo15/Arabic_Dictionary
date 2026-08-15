"""
Repository interfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from arabic_dictionary.domain import Entry


class DictionaryRepository(ABC):
    """Abstract repository."""

    @abstractmethod
    def get(self, word: str) -> Entry | None:
        """Return one entry."""

    @abstractmethod
    def save(self, entry: Entry) -> None:
        """Insert or update."""

    @abstractmethod
    def delete(self, word: str) -> None:
        """Delete an entry."""

    @abstractmethod
    def exists(self, word: str) -> bool:
        """Return True if entry exists."""

    @abstractmethod
    def search(self, text: str) -> list[Entry]:
        """Search entries."""

    @abstractmethod
    def all(self) -> Iterable[Entry]:
        """Return all entries."""

    @abstractmethod
    def count(self) -> int:
        """Number of entries."""

    @abstractmethod
    def clear(self) -> None:
        """Remove all entries."""
