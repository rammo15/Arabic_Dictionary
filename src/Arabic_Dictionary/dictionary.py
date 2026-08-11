from .models import Word


class Dictionary:

    def __init__(self):
        self._providers = []

    def register_provider(self, provider):

        self._providers.append(provider)

    def lookup(self, text: str):

        for provider in self._providers:

            result = provider.lookup(text)

            if result:

                return result

        return None

    def exists(self, text):

        return self.lookup(text) is not None
