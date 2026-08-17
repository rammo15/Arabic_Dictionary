from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from arabic_dictionary.domain import Entry, Sense, WordType

from ..base import Provider


class StaticProvider(Provider):
    """Provider that serves entries from an in-memory dictionary."""

    def __init__(self, entries: dict[str, Entry]) -> None:
        self._entries = entries

    @property
    def name(self) -> str:
        return "static"

    def lookup(self, word: str) -> Entry | None:
        return self._entries.get(word)

    @classmethod
    def from_file(cls, path: str | Path) -> StaticProvider:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            {word: cls._parse_entry(word, entry_data) for word, entry_data in data.items()}
        )

    @staticmethod
    def _parse_entry(word: str, data: dict[str, Any]) -> Entry:
        return Entry(
            text=word,
            source="static",
            root=data.get("root"),
            plural=data.get("plural"),
            senses=[
                Sense(
                    meaning=s["meaning"],
                    word_type=WordType(s["word_type"]) if s.get("word_type") else None,
                    examples=s.get("examples", []),
                    synonyms=s.get("synonyms", []),
                    antonyms=s.get("antonyms", []),
                )
                for s in data.get("senses", [])
            ],
        )
