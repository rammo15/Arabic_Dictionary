from arabic_dictionary.providers import Provider


class DummyProvider(Provider):

    @property
    def name(self) -> str:
        return "dummy"

    def lookup(self, word: str):
        return None


def test_provider_name():
    provider = DummyProvider()

    assert provider.name == "dummy"


def test_lookup_returns_none():
    provider = DummyProvider()

    assert provider.lookup("كتاب") is None