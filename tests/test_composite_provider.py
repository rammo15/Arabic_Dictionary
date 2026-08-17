from __future__ import annotations

from unittest.mock import MagicMock

from arabic_dictionary.domain import Entry, Sense, WordType
from arabic_dictionary.providers import Provider
from arabic_dictionary.providers.composite import CompositeProvider

_KITAB = Entry(
    text="كتاب",
    source="static",
    root="كتب",
    senses=[Sense(meaning="كتاب يُقرأ.", word_type=WordType.NOUN)],
)

_QALAM = Entry(
    text="قلم",
    source="wiktionary",
    senses=[Sense(meaning="أداة للكتابة.")],
)


def _make_provider(name: str, result: Entry | None) -> Provider:
    mock = MagicMock(spec=Provider)
    mock.name = name
    mock.lookup.return_value = result
    return mock


def test_provider_name() -> None:
    composite = CompositeProvider([])
    assert composite.name == "composite"


def test_returns_first_successful_result() -> None:
    p1 = _make_provider("static", _KITAB)
    p2 = _make_provider("wiktionary", _QALAM)
    composite = CompositeProvider([p1, p2])

    entry = composite.lookup("كتاب")

    assert entry is _KITAB


def test_falls_through_to_next_provider_when_first_returns_none() -> None:
    p1 = _make_provider("static", None)
    p2 = _make_provider("wiktionary", _QALAM)
    composite = CompositeProvider([p1, p2])

    entry = composite.lookup("قلم")

    assert entry is _QALAM


def test_returns_none_when_all_providers_return_none() -> None:
    p1 = _make_provider("static", None)
    p2 = _make_provider("wiktionary", None)
    composite = CompositeProvider([p1, p2])

    assert composite.lookup("غير_موجود") is None


def test_stops_at_first_result_and_does_not_call_remaining_providers() -> None:
    p1 = _make_provider("static", _KITAB)
    p2 = _make_provider("wiktionary", _QALAM)
    composite = CompositeProvider([p1, p2])

    composite.lookup("كتاب")

    p2.lookup.assert_not_called()


def test_empty_providers_list_returns_none() -> None:
    composite = CompositeProvider([])

    assert composite.lookup("كتاب") is None


def test_integration_static_first_then_wiktionary_mock() -> None:
    """Static hit → wiktionary never called. Static miss → wiktionary called."""
    from arabic_dictionary.providers.static import StaticProvider

    static = StaticProvider({"كتاب": _KITAB})
    wiki_mock = _make_provider("wiktionary", _QALAM)
    composite = CompositeProvider([static, wiki_mock])

    # Word found in static — wiktionary should not be consulted
    entry = composite.lookup("كتاب")
    assert entry is _KITAB
    wiki_mock.lookup.assert_not_called()

    # Word missing from static — falls through to wiktionary mock
    entry = composite.lookup("قلم")
    assert entry is _QALAM
    wiki_mock.lookup.assert_called_once_with("قلم")
