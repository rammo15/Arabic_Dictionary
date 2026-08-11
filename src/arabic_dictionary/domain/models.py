from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Sense:
    """
    معنى واحد للكلمة.
    """

    meaning: str

    word_type: str | None = None

    examples: list[str] = field(default_factory=list)

    synonyms: list[str] = field(default_factory=list)

    antonyms: list[str] = field(default_factory=list)

    notes: str | None = None


@dataclass(slots=True)
class Entry:
    """
    مدخل معجمي.
    """

    text: str

    root: str | None = None

    plural: str | None = None

    singular: str | None = None

    masculine: str | None = None

    feminine: str | None = None

    pronunciation: str | None = None

    etymology: str | None = None

    source: str | None = None

    senses: list[Sense] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def letters_count(self):

        return len(self.text.replace(" ", ""))

    @property
    def meanings_count(self):

        return len(self.senses)

    def add_sense(self, sense: Sense):

        self.senses.append(sense)

    @property
    def primary_meaning(self):

        if self.senses:

            return self.senses[0].meaning

        return None

    def to_dict(self):

        return {

            "text": self.text,

            "root": self.root,

            "plural": self.plural,

            "singular": self.singular,

            "masculine": self.masculine,

            "feminine": self.feminine,

            "pronunciation": self.pronunciation,

            "etymology": self.etymology,

            "source": self.source,

            "letters_count": self.letters_count,

            "senses": [

                {

                    "meaning": s.meaning,

                    "word_type": s.word_type,

                    "examples": s.examples,

                    "synonyms": s.synonyms,

                    "antonyms": s.antonyms,

                    "notes": s.notes,

                }

                for s in self.senses

            ],

        }
