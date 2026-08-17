from __future__ import annotations

from arabic_dictionary.domain import Entry

from .base import Provider


class CompositeProvider(Provider):
    """Provider that delegates to a list of providers in order."""

    def __init__(self, providers: list[Provider]) -> None:
        self._providers = providers

    @property
    def name(self) -> str:
        return "composite"

    def lookup(self, word: str) -> Entry | None:
        for provider in self._providers:
            entry = provider.lookup(word)
            if entry is not None:
                return entry
        return None
