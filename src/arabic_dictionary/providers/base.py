from __future__ import annotations

from abc import ABC, abstractmethod

from arabic_dictionary.domain import Entry


class Provider(ABC):
    """Abstract dictionary provider."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""

    @abstractmethod
    def lookup(self, word: str) -> Entry | None:
        """Return an entry if found."""