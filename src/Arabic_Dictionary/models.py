from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Sense:
    word_type: str
    meaning: str
    examples: list[str]

    root: str | None = None

    plural: str | None = None

    singular: str | None = None

    masculine: str | None = None

    feminine: str | None = None

    examples: list[str] = field(default_factory=list)

    synonyms: list[str] = field(default_factory=list)

    antonyms: list[str] = field(default_factory=list)

    source: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def letters_count(self) -> int:
        return len(self.text.replace(" ", ""))

    @property
    def has_meaning(self) -> bool:
        return bool(self.meaning)

    @property
    def has_root(self) -> bool:
        return bool(self.root)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "word_type": self.word_type,
            "meaning": self.meaning,
            "root": self.root,
            "plural": self.plural,
            "singular": self.singular,
            "masculine": self.masculine,
            "feminine": self.feminine,
            "examples": self.examples,
            "synonyms": self.synonyms,
            "antonyms": self.antonyms,
            "letters_count": self.letters_count,
            "source": self.source,
            "metadata": self.metadata,
        }

    def __str__(self) -> str:

        lines = [self.text]

        if self.word_type:
            lines.append(f"النوع: {self.word_type}")

        if self.root:
            lines.append(f"الجذر: {self.root}")

        if self.meaning:
            lines.append(f"المعنى: {self.meaning}")

        if self.source:
            lines.append(f"المصدر: {self.source}")

        return "\n".join(lines)
