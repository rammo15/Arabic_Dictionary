from __future__ import annotations

import json
from pathlib import Path

import pytest

from arabic_dictionary.domain import Entry, Sense, WordType
from arabic_dictionary.providers.static import StaticProvider

_KITAB = Entry(
    text="كتاب",
    source="static",
    root="كتب",
    plural="كتب",
    senses=[
        Sense(
            meaning="كتاب يُقرأ.",
            word_type=WordType.NOUN,
            examples=["هذا كتاب مفيد."],
            synonyms=["سفر"],
            antonyms=[],
        )
    ],
)


def test_provider_name() -> None:
    provider = StaticProvider({})
    assert provider.name == "static"


def test_lookup_existing_word() -> None:
    provider = StaticProvider({"كتاب": _KITAB})

    entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.text == "كتاب"
    assert entry.root == "كتب"
    assert entry.plural == "كتب"
    assert len(entry.senses) == 1
    assert entry.senses[0].meaning == "كتاب يُقرأ."
    assert entry.senses[0].word_type == WordType.NOUN
    assert entry.senses[0].synonyms == ["سفر"]


def test_lookup_missing_word_returns_none() -> None:
    provider = StaticProvider({"كتاب": _KITAB})

    assert provider.lookup("قلم") is None


def test_empty_dictionary() -> None:
    provider = StaticProvider({})

    assert provider.lookup("كتاب") is None


def test_from_file_loads_entries(tmp_path: Path) -> None:
    data = {
        "كتاب": {
            "root": "كتب",
            "plural": "كتب",
            "senses": [
                {
                    "meaning": "كتاب يُقرأ.",
                    "word_type": "noun",
                    "examples": ["هذا كتاب مفيد."],
                    "synonyms": ["سفر"],
                    "antonyms": [],
                }
            ],
        }
    }
    path = tmp_path / "words.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    provider = StaticProvider.from_file(path)
    entry = provider.lookup("كتاب")

    assert entry is not None
    assert entry.text == "كتاب"
    assert entry.root == "كتب"
    assert entry.senses[0].word_type == WordType.NOUN


def test_from_file_with_missing_optional_fields(tmp_path: Path) -> None:
    data = {"قلم": {"senses": [{"meaning": "أداة للكتابة."}]}}
    path = tmp_path / "words.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    entry = StaticProvider.from_file(path).lookup("قلم")

    assert entry is not None
    assert entry.root is None
    assert entry.plural is None
    assert entry.senses[0].word_type is None


def test_from_file_invalid_json_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{ not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        StaticProvider.from_file(path)
