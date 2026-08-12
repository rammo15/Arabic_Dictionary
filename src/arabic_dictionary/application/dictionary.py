from __future__ import annotations

from .models import Entry
from .providers import Provider


class Dictionary:
    def __init__(self):

        self.providers: list[Provider] = []

    def add_provider(self, provider: Provider):

        self.providers.append(provider)

    def lookup(self, word: str) -> Entry | None:

        for provider in self.providers:
            result = provider.lookup(word)

            if result is not None:
                return result

        return None

    def exists(self, word: str) -> bool:

        return self.lookup(word) is not None

    def provider_names(self):

        return [p.name for p in self.providers]
